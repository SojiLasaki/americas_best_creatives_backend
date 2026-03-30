from rest_framework import generics, permissions
from .models import SupportTicket
from .serializers import SupportTicketSerializer


class SupportTicketCreateView(generics.CreateAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class SupportTicketListView(generics.ListAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin or user.is_customer_support or user.is_admin:
            return SupportTicket.objects.all()
        return SupportTicket.objects.filter(customer=user)
