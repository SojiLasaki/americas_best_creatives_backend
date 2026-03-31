from django.urls import path
from .views import (
    InvoiceCreateView, InvoiceListView, InvoiceDetailView,
    PaymentCreateView, PaymentVerifyView, PaymentHistoryView, PaymentReceiptView
)

urlpatterns = [
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/<uuid:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/verify/', PaymentVerifyView.as_view(), name='payment-verify'),
    path('payments/history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('payments/<uuid:pk>/receipt/', PaymentReceiptView.as_view(), name='payment-receipt'),
]
