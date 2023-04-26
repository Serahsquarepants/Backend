import django_filters

from API.models import Libro

class LibroFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr='icontains')
    autor = django_filters.CharFilter(lookup_expr='icontains')
    precio_unitario = django_filters.NumberFilter()
    precio_unitario__gt = django_filters.NumberFilter(field_name='precio_unitario', lookup_expr='gt')
    precio_unitario__lt = django_filters.NumberFilter(field_name='precio_unitario', lookup_expr='lt')

    class Meta:
        model = Libro
        fields = ['titulo','autor','precio_unitario','precio_unitario__gt','precio_unitario__lt']
    
