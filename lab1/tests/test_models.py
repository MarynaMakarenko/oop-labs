import unittest
from datetime import date, datetime
from app.models.booking import Booking
from app.models.invoice import Invoice
from app.models.room import Room
from app.models.user import User


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.client = User(id=1, username='alice', password_hash='abc',
                           role='client', full_name='Alice', email='a@b.com')
        self.admin = User(id=2, username='admin', password_hash='xyz',
                          role='admin', full_name='Admin', email='admin@b.com')

    def test_is_client(self):
        self.assertTrue(self.client.is_client())
        self.assertFalse(self.client.is_admin())

    def test_is_admin(self):
        self.assertTrue(self.admin.is_admin())
        self.assertFalse(self.admin.is_client())

    def test_to_dict_excludes_password(self):
        d = self.client.to_dict()
        self.assertNotIn('password_hash', d)
        self.assertEqual(d['username'], 'alice')
        self.assertEqual(d['role'], 'client')

    def test_polymorphism_role_check(self):
        users = [self.client, self.admin]
        admins = [u for u in users if u.is_admin()]
        self.assertEqual(len(admins), 1)


class TestRoomModel(unittest.TestCase):

    def setUp(self):
        self.room = Room(id=1, number='101', capacity=2,
                         apartment_class='standard', price_per_day=100.0)

    def test_defaults(self):
        self.assertTrue(self.room.is_available)
        self.assertEqual(self.room.description, '')

    def test_to_dict(self):
        d = self.room.to_dict()
        self.assertEqual(d['number'], '101')
        self.assertEqual(d['price_per_day'], 100.0)
        self.assertTrue(d['is_available'])


class TestBookingModel(unittest.TestCase):

    def _make(self, check_in, check_out):
        return Booking(id=1, client_id=1, guests_count=2,
                       apartment_class='standard',
                       check_in=date(*check_in), check_out=date(*check_out))

    def test_nights_4(self):
        b = self._make((2024, 6, 1), (2024, 6, 5))
        self.assertEqual(b.nights, 4)

    def test_nights_1(self):
        b = self._make((2024, 6, 1), (2024, 6, 2))
        self.assertEqual(b.nights, 1)

    def test_default_status_pending(self):
        b = self._make((2024, 6, 1), (2024, 6, 3))
        self.assertEqual(b.status, 'pending')

    def test_to_dict_contains_nights(self):
        b = self._make((2024, 7, 10), (2024, 7, 12))
        d = b.to_dict()
        self.assertEqual(d['nights'], 2)
        self.assertEqual(d['status'], 'pending')


class TestInvoiceModel(unittest.TestCase):

    def test_default_status_unpaid(self):
        inv = Invoice(id=1, booking_id=1, amount=400.0)
        self.assertEqual(inv.status, 'unpaid')
        self.assertIsNone(inv.paid_at)

    def test_to_dict(self):
        inv = Invoice(id=1, booking_id=1, amount=250.50)
        d = inv.to_dict()
        self.assertEqual(d['amount'], 250.50)
        self.assertIsNone(d['paid_at'])


if __name__ == '__main__':
    unittest.main()
