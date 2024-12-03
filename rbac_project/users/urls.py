from django.urls import path
from .views import RegisterView, LoginSendOTPView, LoginVerifyOTPView, RefreshTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginSendOTPView.as_view(), name='login_send_otp'),
    path('verify-otp/', LoginVerifyOTPView.as_view(), name='login_verify_otp'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
]
