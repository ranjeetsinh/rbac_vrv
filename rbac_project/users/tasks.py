from django.core.mail import send_mail
from .models import OTP
from celery import shared_task

@shared_task(bind=True, retry_backoff=300)
def send_otp_email(self, user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(id=user_id)

    otp_code = OTP.generate_otp()
    OTP.objects.update_or_create(user=user, defaults={'code': otp_code})

    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp_code}. It will expire in 10 minutes.',
        'your-email@gmail.com',
        [user.email],
        fail_silently=False,
    )