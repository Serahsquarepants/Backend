from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    categoria = serializers.SlugRelatedField(
        slug_field='nombre', queryset=Categoria.objects.all())

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'imagen', 'autor',
                  'descripcion', 'precio_unitario', 'categoria']
        
class PedidoLibroSerializer(serializers.ModelSerializer):
    cantidad = serializers.IntegerField()
    precio_total = serializers.FloatField()
    libro = BookSerializer()

    class Meta:
        model = Pedido_Libro
        fields = ('id', 'cantidad', 'precio_total', 'libro')

class PedidoSerializer(serializers.ModelSerializer):
    libros = PedidoLibroSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ('id', 'precio_pedido', 'fecha_pedido', 'usuario', 'libros', 'estado')



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Usuario
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'address']
        extra_kwargs = {'password': {'write_only': True}}
        
    
    def create(self, validated_data):
        user = Usuario.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['email']
        )
        return user
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

