import random

from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)  # For 2FA

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class OTP(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name='otp')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        expiration_time = self.created_at + timedelta(minutes=10)
        return now() > expiration_time

    @staticmethod
    def generate_otp():
        return f"{random.randint(100000, 999999)}"

    def __str__(self):
        return f"{self.user.email} - {self.code}"
