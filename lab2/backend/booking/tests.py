from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Booking, Invoice, Room, User


class UserModelTest(TestCase):

    def test_is_admin(self):
        u = User(username='a', role='admin')
        self.assertTrue(u.is_admin())
        self.assertFalse(u.is_client())

    def test_is_client(self):
        u = User(username='c', role='client')
        self.assertTrue(u.is_client())
        self.assertFalse(u.is_admin())

    def test_str(self):
        u = User(username='bob', role='client')
        self.assertIn('bob', str(u))


class BookingModelTest(TestCase):

    def setUp(self):
        self.client_user = User.objects.create_user('cli', password='pass', role='client')
        self.room = Room.objects.create(
            number='101', capacity=2, apartment_class='standard', price_per_day=100
        )

    def test_nights_calculation(self):
        b = Booking(
            client=self.client_user, guests_count=1, apartment_class='standard',
            check_in=date(2024, 6, 1), check_out=date(2024, 6, 5)
        )
        self.assertEqual(b.nights, 4)

    def test_default_status(self):
        b = Booking.objects.create(
            client=self.client_user, guests_count=1, apartment_class='standard',
            check_in=date(2024, 6, 1), check_out=date(2024, 6, 3)
        )
        self.assertEqual(b.status, 'pending')


class RoomAPITest(TestCase):

    def setUp(self):
        self.client_api = APIClient()
        self.admin = User.objects.create_user('admin', password='admin123', role='admin')
        self.cli   = User.objects.create_user('user1', password='pass123',  role='client')
        self.room  = Room.objects.create(
            number='201', capacity=2, apartment_class='standard', price_per_day=120
        )

    def _auth(self, user, password):
        resp = self.client_api.post('/api/auth/token/', {'username': user, 'password': password})
        self.client_api.credentials(HTTP_AUTHORIZATION='Bearer ' + resp.data['access'])

    def test_list_rooms_requires_auth(self):
        resp = self.client_api.get('/api/rooms/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_rooms_authenticated(self):
        self._auth('user1', 'pass123')
        resp = self.client_api.get('/api/rooms/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_room_admin_only(self):
        self._auth('user1', 'pass123')
        resp = self.client_api.post('/api/rooms/', {
            'number': '999', 'capacity': 2,
            'apartment_class': 'economy', 'price_per_day': 50
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_room_as_admin(self):
        self._auth('admin', 'admin123')
        resp = self.client_api.post('/api/rooms/', {
            'number': '999', 'capacity': 2,
            'apartment_class': 'economy', 'price_per_day': 50
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


class BookingAPITest(TestCase):

    def setUp(self):
        self.client_api = APIClient()
        self.admin = User.objects.create_user('admin', password='admin123', role='admin')
        self.cli   = User.objects.create_user('user1', password='pass123',  role='client')
        self.room  = Room.objects.create(
            number='101', capacity=2, apartment_class='standard',
            price_per_day=100, is_available=True
        )

    def _auth(self, user, password):
        resp = self.client_api.post('/api/auth/token/', {'username': user, 'password': password})
        self.client_api.credentials(HTTP_AUTHORIZATION='Bearer ' + resp.data['access'])

    def test_client_can_create_booking(self):
        self._auth('user1', 'pass123')
        resp = self.client_api.post('/api/bookings/', {
            'guests_count': 1, 'apartment_class': 'standard',
            'check_in': '2024-07-01', 'check_out': '2024-07-04'
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['status'], 'pending')

    def test_admin_can_approve_booking(self):
        booking = Booking.objects.create(
            client=self.cli, guests_count=1, apartment_class='standard',
            check_in=date(2024, 7, 1), check_out=date(2024, 7, 3)
        )
        self._auth('admin', 'admin123')
        resp = self.client_api.post(f'/api/bookings/{booking.pk}/approve/',
                                    {'room_id': self.room.pk})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 'approved')

        invoice = Invoice.objects.get(booking=booking)
        self.assertEqual(float(invoice.amount), 200.0)
