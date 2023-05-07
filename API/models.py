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
    
    USERNAME_FIELD = 'email' # Cambiar la clave obligatoria a email
    REQUIRED_FIELDS = [] # Eliminar el campo username de los campos requeridos
    
    objects = UsuarioManager() 
    
    def __str__(self):
        return self.email
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=80, blank=False, null=False)
    
    def __str__(self):
        return self.nombre

# class Libro(models.Model):
#     titulo = models.CharField(max_length=150, blank=False, null=False)
#     imagen = models.URLField()
#     autor = models.CharField(max_length=150, blank=False, null=False, default='Desconocido')
#     descripcion = models.TextField(blank=False, null=False)
#     precio_unitario = models.FloatField(blank=False, null=False)
#     categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.titulo

# class Pedido(models.Model):
#     precio_pedido = models.FloatField(blank=False, null=False)
#     fecha_pedido = models.DateField(auto_now_add=True)
#     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
#     libros = models.ManyToManyField(Libro, through='Pedido_Libro')
#     estado = models.BooleanField(default=False)


# class Pedido_Libro(models.Model):
#     cantidad_libros = models.IntegerField()
#     precio_total_libros = models.FloatField()
#     libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
#     pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

class Libro(models.Model):
    titulo = models.CharField(max_length=150, blank=False, null=False)
    imagen = models.URLField()
    autor = models.CharField(max_length=150, blank=False, null=False, default='Desconocido')
    descripcion = models.TextField(blank=False, null=False)
    precio_unitario = models.FloatField(blank=False, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo

class Pedido(models.Model):
    precio_pedido = models.FloatField(blank=False, null=False)
    fecha_pedido = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libros = models.ManyToManyField(Libro, through='Pedido_Libro')
    estado = models.BooleanField(default=False)

class Pedido_Libro(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=False, null=False)
    precio_total = models.FloatField(blank=False, null=False)




