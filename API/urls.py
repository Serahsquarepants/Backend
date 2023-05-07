from django.urls import include, path
from .views import LibroViewSet, LibroDetailView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'libro', LibroViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('libro/<int:pk>', LibroDetailView.as_view(),name='libro_detail')
] 