from django.urls import path
from .views import RegisterView, LoginSendOTPView, LoginVerifyOTPView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/send-otp/', LoginSendOTPView.as_view(), name='login_send_otp'),
    path('login/verify-otp/', LoginVerifyOTPView.as_view(), name='login_verify_otp'),
]
