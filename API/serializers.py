from rest_framework import serializers
from .models import *

class BookSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField()
    
    class Meta:
        model = Libro
        fields = ['titulo','imagen','autor','descripcion','precio_unitario','categoria']
