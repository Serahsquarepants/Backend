import django_filters
from django.db.models import Q
from API.models import Libro

class LibroFilter(django_filters.FilterSet):
    contains = django_filters.CharFilter(method='filtrar_por_contenido')
    categoria = django_filters.CharFilter(field_name='categoria__nombre')

    class Meta:
        model = Libro
        fields = ['contains','categoria']
    
    def filtrar_por_contenido(self, queryset, name, value):
        return queryset.filter(Q(titulo__icontains=value) | Q(autor__icontains=value))