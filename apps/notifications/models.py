from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        QUOTE = 'quote', 'Quote'
        PAYMENT = 'payment', 'Payment'
        DESIGN = 'design', 'Design'
        DISPUTE = 'dispute', 'Dispute'
        SYSTEM = 'system', 'System'
        SUPPORT = 'support', 'Support'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NotificationType.choices, default=NotificationType.SYSTEM)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Notification for {self.user.email}: {self.message[:50]}'
