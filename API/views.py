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

