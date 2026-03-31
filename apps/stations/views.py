from rest_framework import viewsets, permissions
from .models import Station
from .serializers import StationSerializer
from apps.permissions import IsSuperAdmin, IsAdminOrSuperAdmin


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminOrSuperAdmin()]
        return [permissions.IsAuthenticated()]
