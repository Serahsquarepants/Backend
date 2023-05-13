from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
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
    queryset = Libro.objects.filter(cantidad__gt=0)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def partial_update(self,request,*args,**kwargs):
        libro = self.get_object()
        cantidad = request.data.get('cantidad')
        if cantidad is not None:
            if libro.cantidad + cantidad < 0:
                libro.cantidad = 0
            else:
                
                libro.cantidad += cantidad
            libro.save()
            serializer = BookSerializer(libro, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'error': 'La cantidad no puede ser nula.'}, status=status.HTTP_400_BAD_REQUEST)
    


class CategoriaView(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    basename = 'categoria'
    queryset= Categoria.objects.all()
    
    
class LibroDetailView(viewsets.ModelViewSet):
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
    
# No conseguí hacer que funcione, he probado mil y una cosas pero me faltan conocimientos para hacerlo.
        
# class CarritoViewSet(viewsets.ModelViewSet):
#     serializer_class = CarritoSerializer
#     basename = 'carrito'

#     def get_queryset(self):
#         return Carrito.objects.filter(usuario=self.request.user, estado=False)

#     def create(self, request, *args, **kwargs):
#         libro_id = request.data.get('libro')
#         cantidad = request.data.get('cantidad')

#         import ipdb
#         ipdb.set_trace()
#         libro = get_object_or_404(Libro, id=libro_id)

#         carrito, created = Carrito.objects.get_or_create(
#             usuario=request.user,
#             estado=False,
#         )

#         if created:
#             carrito.cantidad = 0
#             carrito.precio_total = 0

#         carrito_libro, created = Carrito.objects.get_or_create(
#             carrito=carrito,
#             libro=libro,
#             defaults={
#                 'cantidad': cantidad,
#                 'precio_total': libro.precio_unitario * cantidad
#             }
#         )

#         if not created:
#             carrito_libro.cantidad += cantidad
#             carrito_libro.precio_total += libro.precio_unitario * cantidad
#             carrito_libro.save()

#         carrito.precio_total += libro.precio_unitario * cantidad
#         carrito.cantidad = sum([cl.cantidad for cl in carrito.carrito_libros.all()])
#         carrito.save()
        
#         serializer = CarritoSerializer(carrito, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()

#         libros_data = request.data.get('libros') if 'libros' in request.data else []

#         # Eliminar todos los libros del carrito actual
#         instance.libro.all().delete()

#         for libro_data in libros_data:
#             libro = Libro.objects.get(id=libro_data['libro']['id'])
#             cantidad = libro_data['cantidad_libros']
#             precio_total = libro.precio_unitario * cantidad
#             # Actualizar la cantidad y el precio total del libro en el carrito actual
#             carrito_libro = Carrito.objects.filter(usuario=request.user, libro=libro).first()
#             if carrito_libro:
#                 carrito_libro.cantidad += cantidad
#                 carrito_libro.precio_total += precio_total
#                 carrito_libro.save()
#             else:
#                 Carrito.objects.create(
#                     usuario=request.user,
#                     libro=libro,
#                     cantidad=cantidad,
#                     precio_total=precio_total,
#                     estado=False
#                 )
#             instance.precio_total += precio_total

#         instance.save()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

    
#     @action(detail=True, methods=['put'])
#     def comprar(self, request, pk=None):
#         carrito = self.get_object()
#         carrito.estado = True
#         carrito.save()
#         serializer = CarritoSerializer(carrito)
#         return Response(serializer.data)

