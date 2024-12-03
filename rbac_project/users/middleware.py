import logging
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.http import JsonResponse

# Define the logger
logger = logging.getLogger(__name__)

class AuditLogMiddleware:
    """
    Middleware to log user actions for auditing purposes.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            user = request.user
            action = None

            # Capture login attempts (successful)
            if request.path == '/login/' and request.method == 'POST':
                action = 'Login Attempt'
            
            # Capture OTP generation
            elif 'otp' in request.path and request.method == 'POST':
                action = 'OTP Generation'
            
            # Capture other actions if needed
            if action:
                logger.info(f"{action} by {user.email} at {now()}")

        return response
