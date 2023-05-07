from django.urls import include, path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'libro', LibroViewSet)
router.register(r'user', UserViewSet,basename='user')
router.register(r'carrito', CarritoViewSet, basename='carrito')

urlpatterns = [
    path('', include(router.urls)),
    path('libro/<int:pk>', LibroDetailView.as_view(),name='libro_detail'),
    # Distinguir entre crear usuario y loguear usuario con una ruta distinta para no solapar el POST
    path('user/<int:pk>/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='user_detail'),
    path('auth/login', UserViewSet.as_view({'post': 'login'}), name='user_login'),
] 