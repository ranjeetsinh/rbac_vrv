import logging

from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .throttles import LoginThrottle
from .serializers import UserSerializer
from .models import CustomUser, OTP
from .utils import send_otp_email

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginSendOTPView(APIView):
    throttle_classes = [LoginThrottle]
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            # Log successful login attempt
            logger.info(f"Login success for {email} at {now()}")
            send_otp_email(user)
            # Log OTP generation
            logger.info(f"OTP sent to {email} at {now()}")
            return Response({'detail': 'OTP sent to your email.'}, status=status.HTTP_200_OK)
        
        # Log failed login attempt
        logger.warning(f"Login failed for {email} at {now()}")
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

 
class LoginVerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp')

        try:
            user = CustomUser.objects.get(email=email)
            otp = user.otp
            if int(otp.code) == otp_code:
                # Log OTP verification success
                logger.info(f"OTP verified successfully for {email} at {now()}")
                refresh = RefreshToken.for_user(user)
                otp.delete()  # Invalidate OTP after successful login
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)

            # Log OTP verification failure
            logger.warning(f"Invalid or expired OTP for {email} at {now()}")
            return Response({'detail': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            # Log user not found
            logger.warning(f"User {email} not found during OTP verification attempt at {now()}")
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


