from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.RegisterView.as_view(),  name='register'),
    path('auth/me/',       views.MeView.as_view(),        name='me'),

    # Rooms
    path('rooms/',         views.RoomListCreateView.as_view(), name='rooms'),
    path('rooms/<int:pk>/',views.RoomDetailView.as_view(),     name='room-detail'),

    # Bookings
    path('bookings/',            views.BookingListCreateView.as_view(), name='bookings'),
    path('bookings/<int:pk>/',   views.BookingDetailView.as_view(),     name='booking-detail'),
    path('bookings/<int:pk>/approve/', views.BookingApproveView.as_view(), name='booking-approve'),
    path('bookings/<int:pk>/reject/',  views.BookingRejectView.as_view(),  name='booking-reject'),

    # Invoices
    path('invoices/',            views.InvoiceListView.as_view(), name='invoices'),
    path('invoices/<int:pk>/pay/', views.InvoicePayView.as_view(), name='invoice-pay'),
]
