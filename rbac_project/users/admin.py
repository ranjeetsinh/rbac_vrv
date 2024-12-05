from django.contrib import admin
from .models import OTP, CustomUser, Profile, Task
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')

# OTP Admin
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at')
    search_fields = ('user__email',)
    list_filter = ('created_at',)

admin.site.register(Profile)

admin.site.register(Task)