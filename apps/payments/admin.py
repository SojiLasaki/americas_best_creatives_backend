from django.contrib import admin
from .models import Invoice, Payment, PaymentReceipt


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'quote', 'total', 'payment_status', 'due_date', 'created_at')
    list_filter = ('payment_status',)
    search_fields = ('invoice_number',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'customer', 'amount', 'payment_method', 'payment_status', 'paid_at')
    list_filter = ('payment_status', 'payment_method')


@admin.register(PaymentReceipt)
class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ('payment', 'generated_at')
