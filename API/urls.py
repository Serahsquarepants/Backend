from django.urls import include, path
from .views import LibroViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'libro', LibroViewSet)


urlpatterns = [
    path('', include(router.urls)),
] 