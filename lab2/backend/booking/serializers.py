import logging

from django.utils import timezone
from rest_framework import serializers

from .models import Booking, Invoice, Room, User

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email', 'role')
        read_only_fields = ('id',)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ('username', 'password', 'full_name', 'email', 'role')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        logger.info("Registered new user: %s", user.username)
        return user


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number', 'capacity', 'apartment_class',
                  'price_per_day', 'is_available', 'description', 'created_at')
        read_only_fields = ('id', 'created_at')


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('id', 'booking', 'amount', 'status', 'issued_at', 'paid_at')
        read_only_fields = ('id', 'booking', 'amount', 'issued_at')


class BookingSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer(read_only=True)
    nights  = serializers.IntegerField(read_only=True)
    client_username = serializers.CharField(source='client.username', read_only=True)
    room_number     = serializers.CharField(source='room.number', read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'client', 'client_username', 'room', 'room_number',
                  'guests_count', 'apartment_class', 'check_in', 'check_out',
                  'nights', 'status', 'notes', 'created_at', 'invoice')
        read_only_fields = ('id', 'client', 'status', 'room', 'created_at')

    def validate(self, data):
        if data.get('check_out') and data.get('check_in'):
            if data['check_out'] <= data['check_in']:
                raise serializers.ValidationError('check_out must be after check_in')
        return data


class BookingApproveSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()

    def validate_room_id(self, value):
        try:
            room = Room.objects.get(pk=value, is_available=True)
        except Room.DoesNotExist:
            raise serializers.ValidationError('Room not found or not available')
        return value
