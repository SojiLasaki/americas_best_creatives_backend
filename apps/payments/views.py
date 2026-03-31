from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Invoice, Payment, PaymentReceipt
from .serializers import InvoiceSerializer, PaymentSerializer, PaymentReceiptSerializer
from apps.services import InvoiceService, PaymentVerificationService
from apps.permissions import IsAccountant, IsAdminOrSuperAdmin


class InvoiceCreateView(generics.CreateAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(accountant=self.request.user)


class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin or user.is_accountant or user.is_admin:
            return Invoice.objects.all().select_related('quote')
        return Invoice.objects.filter(quote__customer=user).select_related('quote')


class InvoiceDetailView(generics.RetrieveAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin or user.is_accountant or user.is_admin:
            return Invoice.objects.all()
        return Invoice.objects.filter(quote__customer=user)


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class PaymentVerifyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        payment_id = request.data.get('payment_id')
        transaction_id = request.data.get('transaction_id')
        payment = PaymentVerificationService.verify(payment_id, transaction_id)
        return Response(PaymentSerializer(payment).data)


class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin or user.is_accountant:
            return Payment.objects.all()
        return Payment.objects.filter(customer=user)


class PaymentReceiptView(generics.RetrieveAPIView):
    serializer_class = PaymentReceiptSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        payment = get_object_or_404(Payment, pk=self.kwargs['pk'])
        receipt, _ = PaymentReceipt.objects.get_or_create(payment=payment)
        return receipt
