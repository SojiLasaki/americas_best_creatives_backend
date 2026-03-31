from rest_framework import serializers
from .models import Invoice, Payment, PaymentReceipt


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            'id', 'quote', 'invoice_number', 'accountant', 'amount', 'tax', 'total',
            'payment_status', 'due_date', 'created_at',
        )
        read_only_fields = ('invoice_number', 'created_at')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id', 'invoice', 'customer', 'payment_method', 'amount',
            'transaction_id', 'payment_status', 'paid_at', 'created_at',
        )
        read_only_fields = ('customer', 'created_at', 'paid_at')


class PaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentReceipt
        fields = ('id', 'payment', 'receipt_file', 'generated_at')
        read_only_fields = ('generated_at',)
