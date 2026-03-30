"""
Platform-level Django signals.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='quotes.Quote')
def handle_quote_status_change(sender, instance, created, **kwargs):
    from apps.services import NotificationService
    if not created and instance.status == 'awaiting_payment':
        NotificationService.notify(
            user=instance.customer,
            notification_type='payment',
            message=f'Quote #{instance.pk} is ready for payment. Please proceed to checkout.',
        )


@receiver(post_save, sender='payments.Invoice')
def handle_invoice_created(sender, instance, created, **kwargs):
    from apps.services import NotificationService
    if created:
        NotificationService.notify(
            user=instance.quote.customer,
            notification_type='payment',
            message=f'Invoice {instance.invoice_number} has been created for Quote #{instance.quote.pk}.',
        )


@receiver(post_save, sender='designs.DesignSubmission')
def handle_design_submission(sender, instance, created, **kwargs):
    from apps.services import NotificationService
    if created:
        quote = instance.assignment.quote
        NotificationService.notify(
            user=quote.customer,
            notification_type='design',
            message=f'A new design draft has been uploaded for your Quote #{quote.pk}. Please review.',
        )
