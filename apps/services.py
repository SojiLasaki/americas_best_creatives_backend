"""
Business logic services for the ABC Printing Platform.
"""
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class QuoteService:
    """Handles quote creation and related business logic."""

    @staticmethod
    def create_quote(customer, catalog, station, submitted_snapshot, input_values=None, agent=None):
        from apps.quotes.models import Quote, QuoteInputValue
        quote = Quote.objects.create(
            customer=customer,
            catalog=catalog,
            station=station,
            submitted_snapshot=submitted_snapshot,
            created_by_agent=agent,
        )
        if input_values:
            for iv in input_values:
                QuoteInputValue.objects.create(quote=quote, **iv)
        NotificationService.notify(
            user=customer,
            notification_type='quote',
            message=f'Your quote #{quote.pk} has been submitted and is under review.',
        )
        return quote


class QuoteApprovalService:
    """Handles quote approval/rejection by customers."""

    @staticmethod
    def approve(quote, user):
        from apps.quotes.models import Quote
        quote.status = Quote.Status.AWAITING_PAYMENT
        quote.save()
        NotificationService.notify(
            user=quote.customer,
            notification_type='quote',
            message=f'Quote #{quote.pk} approved. Please complete your payment.',
        )
        return 'Quote approved. Awaiting payment.'

    @staticmethod
    def reject(quote, user):
        from apps.quotes.models import Quote
        quote.status = Quote.Status.REJECTED
        quote.save()
        NotificationService.notify(
            user=quote.customer,
            notification_type='quote',
            message=f'Quote #{quote.pk} has been rejected.',
        )
        return 'Quote rejected.'


class InvoiceService:
    """Handles invoice generation."""

    @staticmethod
    def generate(quote, amount, tax=0, due_date=None, accountant=None):
        from apps.payments.models import Invoice
        invoice = Invoice.objects.create(
            quote=quote,
            amount=amount,
            tax=tax,
            total=amount + tax,
            due_date=due_date,
            accountant=accountant,
        )
        NotificationService.notify(
            user=quote.customer,
            notification_type='payment',
            message=f'Invoice {invoice.invoice_number} generated for Quote #{quote.pk}. Amount due: {invoice.total}.',
        )
        return invoice


class PaymentVerificationService:
    """Handles payment verification."""

    @staticmethod
    def verify(payment_id, transaction_id):
        from apps.payments.models import Payment, PaymentReceipt
        try:
            payment = Payment.objects.get(pk=payment_id)
        except Payment.DoesNotExist:
            raise ValueError(f'Payment {payment_id} not found.')

        payment.transaction_id = transaction_id
        payment.payment_status = Payment.PaymentStatus.SUCCESS
        payment.paid_at = timezone.now()
        payment.save()

        # Update invoice status
        invoice = payment.invoice
        invoice.payment_status = invoice.PaymentStatus.PAID
        invoice.save()

        # Update quote status
        quote = invoice.quote
        from apps.quotes.models import Quote
        quote.status = Quote.Status.PAID
        quote.save()

        # Generate receipt
        PaymentReceipt.objects.get_or_create(payment=payment)

        # Notify accountant
        if invoice.accountant:
            NotificationService.notify(
                user=invoice.accountant,
                notification_type='payment',
                message=f'Payment received for Invoice {invoice.invoice_number}.',
            )

        NotificationService.notify(
            user=payment.customer,
            notification_type='payment',
            message=f'Payment confirmed for Invoice {invoice.invoice_number}.',
        )

        return payment


class DesignerAssignmentService:
    """Handles designer assignment with auto-selection logic."""

    @staticmethod
    def auto_select(quote):
        """
        Auto-assign designer based on:
        1. Same station as the quote
        2. Expertise match (catalog name)
        3. Lowest active task count
        4. available = True
        """
        from apps.designs.models import AvailabilityProfile
        qs = AvailabilityProfile.objects.filter(available=True).select_related('designer__profile')

        # Filter by same station
        if quote.station:
            station_designers = qs.filter(designer__profile__station=quote.station)
            if station_designers.exists():
                qs = station_designers

        # Filter by expertise match (catalog name in expertise list)
        if quote.catalog:
            catalog_name = quote.catalog.name.lower()
            expertise_match = [ap for ap in qs if any(
                catalog_name in str(e).lower() for e in ap.expertise
            )]
            if expertise_match:
                qs = expertise_match

        # Sort by active_tasks_count and pick the best
        if hasattr(qs, 'order_by'):
            best = qs.order_by('active_tasks_count').first()
        else:
            best = sorted(qs, key=lambda ap: ap.active_tasks_count)[0] if qs else None

        return best.designer if best else None

    @staticmethod
    def assign(quote, assigned_by, designer_id=None):
        from apps.designs.models import DesignerAssignment, AvailabilityProfile
        from apps.quotes.models import Quote

        if designer_id:
            designer = User.objects.get(pk=designer_id)
        else:
            designer = DesignerAssignmentService.auto_select(quote)

        if not designer:
            raise ValueError('No available designer found.')

        assignment = DesignerAssignment.objects.create(
            quote=quote,
            designer=designer,
            assigned_by=assigned_by,
        )

        # Update availability profile
        try:
            profile = designer.availability
            profile.active_tasks_count += 1
            profile.save()
        except Exception:
            pass

        # Update quote status
        quote.status = Quote.Status.DESIGN_IN_PROGRESS
        quote.save()

        NotificationService.notify(
            user=designer,
            notification_type='design',
            message=f'You have been assigned a design task for Quote #{quote.pk}.',
        )
        NotificationService.notify(
            user=quote.customer,
            notification_type='design',
            message=f'A designer has been assigned to your Quote #{quote.pk}.',
        )

        return assignment


class NotificationService:
    """Handles in-app notifications."""

    @staticmethod
    def notify(user, notification_type, message):
        from apps.notifications.models import Notification
        return Notification.objects.create(
            user=user,
            type=notification_type,
            message=message,
        )


class DisputeEscalationService:
    """Handles dispute creation and escalation."""

    @staticmethod
    def escalate(dispute):
        from apps.quotes.models import Quote

        # Update quote status to disputed
        dispute.quote.status = Quote.Status.DISPUTED
        dispute.quote.save()

        # Notify customer support team
        support_users = User.objects.filter(role=User.Role.CUSTOMER_SUPPORT)
        for support_user in support_users:
            NotificationService.notify(
                user=support_user,
                notification_type='dispute',
                message=f'New dispute #{dispute.pk} raised for Quote #{dispute.quote.pk}.',
            )

        NotificationService.notify(
            user=dispute.customer,
            notification_type='dispute',
            message=f'Your dispute #{dispute.pk} has been submitted and is under review.',
        )

        return dispute
