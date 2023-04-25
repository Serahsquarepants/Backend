from django.db import models
from django.contrib.auth.models import AbstractUser

"""
Se utiliza el modelo propio CustomUser para añadir la dirección del usuario (u otros datos que
puedan hacer falta). Al hacer herencia de AbstractUser se dispone de los datos de User (el por
defecto de Django) y le añadimos un atributo más.
"""
class Usuario(AbstractUser):
    adress = models.CharField(max_length=250, blank=True, null=True)
    
class Pedido(models.Model):
    precio_pedido = models.FloatField(blank=False, null=False)
    fecha_pedido = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=80, blank=False, null=False)

class Libro(models.Model):
    titulo = models.CharField(max_length=150, blank=False, null=False)
    imagen = models.URLField()
    autor = models.CharField(max_length=150, blank=False, null=False, default='Desconocido')
    descripcion = models.TextField(blank=False, null=False)
    precio_unitario = models.FloatField(blank=False, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class Pedido_Libro(models.Model):
    cantidad_libros = models.IntegerField()
    precio_total_libros = models.FloatField()
    estado = models.BooleanField(default=False)