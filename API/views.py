from rest_framework.response import Response
from rest_framework import viewsets

from API.permissions import IsAdminOrReadOnly
from .models import *
from API.serializers import *
from .filters import *

class LibroViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = BookSerializer
    filterset_class = LibroFilter
    queryset = Libro.objects.all()
    