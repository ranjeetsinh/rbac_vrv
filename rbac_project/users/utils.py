from django.core.mail import send_mail
from .models import OTP

def send_otp_email(user):
    otp_code = OTP.generate_otp()
    OTP.objects.update_or_create(user=user, defaults={'code': otp_code})

    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp_code}. It will expire in 10 minutes.',
        'your-email@gmail.com',
        [user.email],
        fail_silently=False,
    )