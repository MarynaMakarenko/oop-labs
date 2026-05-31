from django.contrib import admin
from .models import Booking, Invoice, Room, User

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Invoice)
