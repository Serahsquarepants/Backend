from django.contrib import admin
from .models import Usuario, Categoria, Libro



# Registrar los modelos en el admin
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Libro)
# admin.site.register(Carrito)
