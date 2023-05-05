from rest_framework import serializers
from .models import *

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    categoria = serializers.SlugRelatedField(slug_field='nombre', queryset=Categoria.objects.all())
    
    class Meta:
        model = Libro
        fields = ['id','titulo','imagen','autor','descripcion','precio_unitario','categoria']
