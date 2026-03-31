from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationViewSet

router = DefaultRouter()
router.register('stations', StationViewSet, basename='station')

urlpatterns = router.urls
