from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Quote


@receiver(post_save, sender=Quote)
def handle_quote_save(sender, instance, created, **kwargs):
    from apps.services import NotificationService
    if created:
        NotificationService.notify(
            user=instance.customer,
            notification_type='quote',
            message=f'Your quote #{instance.pk} has been submitted successfully.',
        )
    elif instance.status == Quote.Status.AWAITING_PAYMENT:
        NotificationService.notify(
            user=instance.customer,
            notification_type='payment',
            message=f'Your quote #{instance.pk} has been approved. Please proceed with payment.',
        )
