from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from API.permissions import IsAdminOrReadOnly
from .models import *
from API.serializers import *
from .filters import *

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

class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    
    def get_queryset(self, request, *args, **kwargs):
        