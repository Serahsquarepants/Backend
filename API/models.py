from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UsuarioManager

"""
Se utiliza el modelo propio CustomUser para añadir la dirección del usuario (u otros datos que
puedan hacer falta). Al hacer herencia de AbstractUser se dispone de los datos de User (el por
defecto de Django) y le añadimos un atributo más.
"""

class Usuario(AbstractUser):
    address = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []
    
    objects = UsuarioManager() 
    
    def __str__(self):
        return self.email
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=80, blank=False, null=False)
    
    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=150, blank=False, null=False)
    imagen = models.URLField()
    autor = models.CharField(max_length=150, blank=False, null=False, default='Desconocido')
    descripcion = models.TextField(blank=False, null=False)
    precio_unitario = models.FloatField(blank=False, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo


# class Carrito(models.Model):
#     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
#     libro = models.ForeignKey(Libro, on_delete=models.CASCADE, null=True)
#     cantidad = models.IntegerField(blank=False, default=0)
#     precio_total = models.FloatField(blank=False, default=0)
#     estado = models.BooleanField(default=False)




