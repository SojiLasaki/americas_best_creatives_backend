from rest_framework import viewsets, permissions
from .models import Catalog, CatalogInputField
from .serializers import CatalogSerializer, CatalogInputFieldSerializer
from apps.permissions import IsAdminOrSuperAdmin


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.filter(active=True)
    serializer_class = CatalogSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminOrSuperAdmin()]
        return [permissions.IsAuthenticated()]


class CatalogFieldViewSet(viewsets.ModelViewSet):
    serializer_class = CatalogInputFieldSerializer

    def get_queryset(self):
        return CatalogInputField.objects.filter(catalog_id=self.kwargs['catalog_pk'])

    def perform_create(self, serializer):
        serializer.save(catalog_id=self.kwargs['catalog_pk'])

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminOrSuperAdmin()]
        return [permissions.IsAuthenticated()]
