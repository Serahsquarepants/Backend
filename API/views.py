from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from API.permissions import *
from .models import *
from API.serializers import *
from .filters import *
from rest_framework.views import APIView

class LibroViewSet(viewsets.ModelViewSet):
    # Security: Activate before publishing on production.
    # permission_classes = [IsAdminOrReadOnly]
    serializer_class = BookSerializer
    filterset_class = LibroFilter
    queryset = Libro.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LibroDetailView(APIView):
    serializer_class = BookSerializer
    
    def get_queryset(self, request, *args, **kwargs):
        try:
            libro = Libro.objects.get(pk=kwargs['pk'])
        except Libro.DoesNotExist:
            return Response({'message': 'Libro no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(libro)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    basename = 'user'

    def get_queryset(self):
        return Usuario.objects.filter(pk=self.request.user.pk)

    def create(self, request):
        email = request.data.get('email')
        if Usuario.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.username = email
            user.save()
            serializer = UserSerializer(user)
            response_data = serializer.data.copy()
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        user = get_object_or_404(Usuario, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['POST'], detail=False)
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        
        
class CarritoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    basename = 'carrito'

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user, estado=False)

    def create(self, request, *args, **kwargs):
        libros_data = request.data.get('libros') if 'libros' in request.data else []

        pedido = Pedido.objects.filter(usuario=request.user, estado=False).first()
        if not pedido:
            pedido = Pedido.objects.create(
                usuario=request.user,
                precio_pedido=0
            )

        for libro_data in libros_data:
            libro = Libro.objects.get(id=libro_data['libro']['id'])
            cantidad = libro_data['cantidad_libros']

            pedido_libro, created = Pedido_Libro.objects.get_or_create(
                pedido=pedido,
                libro=libro,
                defaults={
                    'cantidad': cantidad,
                    'precio_total': libro.precio_unitario * cantidad
                }
            )

            if not created:
                pedido_libro.cantidad += cantidad
                pedido_libro.precio_total += libro.precio_unitario * cantidad
                pedido_libro.save()

            pedido.precio_pedido += libro.precio_unitario * cantidad

        pedido.save()
        serializer = self.serializer_class(pedido)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        libros_data = request.data.get('libros') if 'libros' in request.data else []

        instance.libros.all().delete()

        for libro_data in libros_data:
            libro = Libro.objects.get(id=libro_data['libro']['id'])
            cantidad = libro_data['cantidad_libros']
            precio_total = libro.precio_unitario * cantidad
            Pedido_Libro.objects.create(
                pedido=instance,
                libro=libro,
                cantidad=cantidad,
                precio_total=precio_total
            )
            instance.precio_pedido += precio_total

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['put'])
    def comprar(self, request, pk=None):
        pedido = self.get_object()
        pedido.estado = True
        pedido.save()
        serializer = self.serializer_class(pedido)
        return Response(serializer.data)
