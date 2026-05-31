import logging

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Invoice, Room, User
from .permissions import IsAdmin, IsClient, IsOwnerOrAdmin
from .serializers import (
    BookingApproveSerializer,
    BookingSerializer,
    InvoiceSerializer,
    RoomSerializer,
    UserRegisterSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)


# ── Auth ─────────────────────────────────────────────────────────────────────

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# ── Rooms ─────────────────────────────────────────────────────────────────────

class RoomListCreateView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.all().order_by('number')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAuthenticated()]


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdmin()]

    def perform_destroy(self, instance):
        logger.info("Admin %s deleted room %s", self.request.user, instance.number)
        instance.delete()


# ── Bookings ──────────────────────────────────────────────────────────────────

class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Booking.objects.select_related('client', 'room').order_by('-created_at')
        return Booking.objects.filter(client=user).select_related('room').order_by('-created_at')

    def perform_create(self, serializer):
        if not self.request.user.is_client():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only clients can create bookings')
        booking = serializer.save(client=self.request.user)
        logger.info("Booking #%s created by %s", booking.pk, self.request.user)


class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return Booking.objects.select_related('client', 'room').prefetch_related('invoice')


class BookingApproveView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        booking = generics.get_object_or_404(Booking, pk=pk, status='pending')
        ser = BookingApproveSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        room = Room.objects.get(pk=ser.validated_data['room_id'])
        booking.room = room
        booking.status = 'approved'
        booking.save()

        room.is_available = False
        room.save()

        amount = booking.nights * room.price_per_day
        Invoice.objects.create(booking=booking, amount=amount)

        logger.info("Admin %s approved booking #%s, room %s, invoice $%s",
                    request.user, booking.pk, room.number, amount)
        return Response(BookingSerializer(booking).data)


class BookingRejectView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        booking = generics.get_object_or_404(Booking, pk=pk, status='pending')
        booking.status = 'rejected'
        booking.save()
        logger.info("Admin %s rejected booking #%s", request.user, booking.pk)
        return Response(BookingSerializer(booking).data)


# ── Invoices ──────────────────────────────────────────────────────────────────

class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Invoice.objects.select_related('booking').order_by('-issued_at')
        return Invoice.objects.filter(
            booking__client=user
        ).select_related('booking').order_by('-issued_at')


class InvoicePayView(APIView):
    permission_classes = [IsClient]

    def post(self, request, pk):
        invoice = generics.get_object_or_404(
            Invoice, pk=pk, status='unpaid', booking__client=request.user
        )
        invoice.status = 'paid'
        invoice.paid_at = timezone.now()
        invoice.save()
        logger.info("Client %s paid invoice #%s", request.user, invoice.pk)
        return Response(InvoiceSerializer(invoice).data)
