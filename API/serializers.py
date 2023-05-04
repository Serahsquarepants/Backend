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
        fields = ['titulo','imagen','autor','descripcion','precio_unitario','categoria']

class UserSerializer(serializer.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ['username','first_name','last_name','address','email','password']
        extra_kwargs = {
            'password' : {write_only: True}
        }
