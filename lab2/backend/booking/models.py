import logging

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

logger = logging.getLogger(__name__)

APARTMENT_CLASSES = [('economy', 'Economy'), ('standard', 'Standard'), ('luxury', 'Luxury')]
BOOKING_STATUSES  = [('pending', 'Pending'), ('approved', 'Approved'),
                     ('rejected', 'Rejected'), ('completed', 'Completed')]
INVOICE_STATUSES  = [('unpaid', 'Unpaid'), ('paid', 'Paid')]
ROLES             = [('client', 'Client'), ('admin', 'Admin')]


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra):
        user = self.model(username=username, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra):
        extra.setdefault('role', 'admin')
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    """System user; role determines client vs admin access."""

    username  = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=200, blank=True)
    email     = models.EmailField(blank=True)
    role      = models.CharField(max_length=20, choices=ROLES, default='client')
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def is_admin(self) -> bool:
        return self.role == 'admin'

    def is_client(self) -> bool:
        return self.role == 'client'

    def __str__(self):
        return f'{self.username} ({self.role})'


class Room(models.Model):
    """A hotel room available for booking."""

    number          = models.CharField(max_length=20, unique=True)
    capacity        = models.PositiveIntegerField()
    apartment_class = models.CharField(max_length=20, choices=APARTMENT_CLASSES)
    price_per_day   = models.DecimalField(max_digits=10, decimal_places=2)
    is_available    = models.BooleanField(default=True)
    description     = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Room {self.number} ({self.apartment_class})'


class Booking(models.Model):
    """
    A client booking request.

    Created by a client; assigned a room and approved/rejected by admin.
    """

    client          = models.ForeignKey(User, on_delete=models.CASCADE,
                                        related_name='bookings', limit_choices_to={'role': 'client'})
    room            = models.ForeignKey(Room, on_delete=models.SET_NULL,
                                        null=True, blank=True, related_name='bookings')
    guests_count    = models.PositiveIntegerField()
    apartment_class = models.CharField(max_length=20, choices=APARTMENT_CLASSES)
    check_in        = models.DateField()
    check_out       = models.DateField()
    status          = models.CharField(max_length=20, choices=BOOKING_STATUSES, default='pending')
    notes           = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    @property
    def nights(self) -> int:
        return max((self.check_out - self.check_in).days, 0)

    def __str__(self):
        return f'Booking #{self.pk} by {self.client} [{self.status}]'


class Invoice(models.Model):
    """Financial invoice generated after a booking is approved."""

    booking   = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='invoice')
    amount    = models.DecimalField(max_digits=10, decimal_places=2)
    status    = models.CharField(max_length=20, choices=INVOICE_STATUSES, default='unpaid')
    issued_at = models.DateTimeField(auto_now_add=True)
    paid_at   = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Invoice #{self.pk} — ${self.amount} [{self.status}]'
