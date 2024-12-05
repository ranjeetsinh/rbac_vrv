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


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    def __str__(self):
        return f'Profile of {self.user.email}'


class OTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='otp')
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


class Task(models.Model):
    summary = models.TextField(null=True, blank=True)
    remind_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='created_task', blank=True, null=True
    )
    created_by_system = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['updated_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['remind_at']),
        ]
        