from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/auth/token/',         TokenObtainPairView.as_view(),  name='token_obtain'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(),     name='token_refresh'),
    path('api/', include('booking.urls')),
]
