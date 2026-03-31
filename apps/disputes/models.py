import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Dispute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        UNDER_REVIEW = 'under_review', 'Under Review'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'

    quote = models.ForeignKey('quotes.Quote', on_delete=models.CASCADE, related_name='disputes')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disputes')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    handled_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_disputes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Dispute #{self.pk} on Quote #{self.quote.pk} ({self.status})'
