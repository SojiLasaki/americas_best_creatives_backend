from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CatalogViewSet, CatalogFieldViewSet

router = DefaultRouter()
router.register('catalog', CatalogViewSet, basename='catalog')

urlpatterns = router.urls + [
    path(
        'catalog/<uuid:catalog_pk>/fields/',
        CatalogFieldViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='catalog-fields',
    ),
    path(
        'catalog/<uuid:catalog_pk>/fields/<uuid:pk>/',
        CatalogFieldViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
        name='catalog-field-detail',
    ),
]
