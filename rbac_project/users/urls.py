from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, 
    LoginSendOTPView, 
    LoginVerifyOTPView, 
    RefreshTokenView,
    ProfileViewSet, 
    TaskViewSet
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginSendOTPView.as_view(), name='login_send_otp'),
    path('verify-otp/', LoginVerifyOTPView.as_view(), name='login_verify_otp'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('', include(router.urls)),
]