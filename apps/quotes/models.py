import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        QUOTED = 'quoted', 'Quoted'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        AWAITING_PAYMENT = 'awaiting_payment', 'Awaiting Payment'
        PAID = 'paid', 'Paid'
        DESIGN_IN_PROGRESS = 'design_in_progress', 'Design In Progress'
        REVISION_REQUESTED = 'revision_requested', 'Revision Requested'
        DISPUTED = 'disputed', 'Disputed'
        COMPLETED = 'completed', 'Completed'

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_quotes')
    station = models.ForeignKey('stations.Station', on_delete=models.CASCADE, related_name='quotes', null=True, blank=True)
    catalog = models.ForeignKey('catalog.Catalog', on_delete=models.SET_NULL, null=True, blank=True)
    created_by_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_quotes')
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.PENDING)
    submitted_snapshot = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Quote #{self.pk} - {self.customer.email} ({self.status})'


class QuoteInputValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='input_values')
    field = models.ForeignKey('catalog.CatalogInputField', on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return f'Quote #{self.quote.pk} - {self.field.field_key}: {self.value}'


class QuoteDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='quote_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Document for Quote #{self.quote.pk}'
