from rest_framework import generics, permissions
from .models import Dispute
from .serializers import DisputeSerializer
from apps.services import DisputeEscalationService


class DisputeCreateView(generics.CreateAPIView):
    serializer_class = DisputeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        dispute = serializer.save(customer=self.request.user)
        DisputeEscalationService.escalate(dispute)


class DisputeListView(generics.ListAPIView):
    serializer_class = DisputeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin or user.is_customer_support or user.is_admin:
            return Dispute.objects.all()
        return Dispute.objects.filter(customer=user)
