from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.stations.models import Station
from apps.catalog.models import Catalog, CatalogInputField
from apps.quotes.models import Quote
from apps.notifications.models import Notification

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.station = Station.objects.create(name='Main', location='New York', code='NY001')
        self.customer = User.objects.create_user(
            email='customer@example.com',
            password='testpass123',
            full_name='Test Customer',
            role=User.Role.CUSTOMER,
        )
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            full_name='Test Admin',
            role=User.Role.ADMIN,
        )
        self.designer = User.objects.create_user(
            email='designer@example.com',
            password='designerpass123',
            full_name='Test Designer',
            role=User.Role.DESIGNER,
        )

    def test_user_roles(self):
        self.assertTrue(self.customer.is_customer)
        self.assertFalse(self.customer.is_admin)
        self.assertTrue(self.admin.is_admin)
        self.assertTrue(self.designer.is_designer)

    def test_profile_created_on_user_save(self):
        self.assertIsNotNone(self.customer.profile)

    def test_station_model(self):
        self.assertEqual(str(self.station), 'Main (NY001)')


class CatalogModelTest(TestCase):
    def test_catalog_slug_auto_generated(self):
        catalog = Catalog.objects.create(name='Business Cards', category='print')
        self.assertEqual(catalog.slug, 'business-cards')

    def test_catalog_input_field(self):
        catalog = Catalog.objects.create(name='Flyers', category='print')
        field = CatalogInputField.objects.create(
            catalog=catalog,
            label='Quantity',
            field_key='quantity',
            field_type=CatalogInputField.FieldType.NUMBER,
            required=True,
        )
        self.assertEqual(str(field), 'Flyers - Quantity')


class QuoteModelTest(TestCase):
    def setUp(self):
        self.station = Station.objects.create(name='Main', location='NYC', code='NYC01')
        self.catalog = Catalog.objects.create(name='Business Cards', category='print')
        self.customer = User.objects.create_user(
            email='cust@test.com', password='pass', full_name='Customer', role=User.Role.CUSTOMER
        )

    def test_quote_creation(self):
        quote = Quote.objects.create(
            customer=self.customer,
            station=self.station,
            catalog=self.catalog,
            status=Quote.Status.PENDING,
        )
        self.assertEqual(quote.status, Quote.Status.PENDING)
        self.assertEqual(quote.customer, self.customer)

    def test_quote_statuses(self):
        self.assertEqual(Quote.Status.PENDING, 'pending')
        self.assertEqual(Quote.Status.APPROVED, 'approved')
        self.assertEqual(Quote.Status.COMPLETED, 'completed')


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='notify@test.com', password='pass', full_name='Notify User'
        )

    def test_notification_created(self):
        notif = Notification.objects.create(
            user=self.user,
            type=Notification.NotificationType.QUOTE,
            message='Your quote is ready.',
        )
        self.assertFalse(notif.is_read)
        self.assertEqual(notif.user, self.user)


class ServicesTest(TestCase):
    def setUp(self):
        self.station = Station.objects.create(name='Test Station', location='LA', code='LA001')
        self.customer = User.objects.create_user(
            email='svc_customer@test.com', password='pass', full_name='Service Customer', role=User.Role.CUSTOMER
        )
        self.catalog = Catalog.objects.create(name='Banners', category='print')

    def test_notification_service(self):
        from apps.services import NotificationService
        notif = NotificationService.notify(self.customer, 'quote', 'Test message')
        self.assertEqual(notif.message, 'Test message')
        self.assertEqual(notif.user, self.customer)

    def test_quote_approval_service(self):
        from apps.services import QuoteApprovalService
        quote = Quote.objects.create(
            customer=self.customer,
            station=self.station,
            catalog=self.catalog,
            status=Quote.Status.QUOTED,
        )
        QuoteApprovalService.approve(quote, self.customer)
        quote.refresh_from_db()
        self.assertEqual(quote.status, Quote.Status.AWAITING_PAYMENT)

    def test_quote_rejection_service(self):
        from apps.services import QuoteApprovalService
        quote = Quote.objects.create(
            customer=self.customer,
            station=self.station,
            catalog=self.catalog,
            status=Quote.Status.QUOTED,
        )
        QuoteApprovalService.reject(quote, self.customer)
        quote.refresh_from_db()
        self.assertEqual(quote.status, Quote.Status.REJECTED)
