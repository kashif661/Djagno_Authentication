# authentication/urls.py

from django.urls import path
from .views import UserRegistrationView, VerifyEmailView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
]
