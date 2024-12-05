import logging

from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions

from .throttles import LoginThrottle
from .serializers import UserSerializer, ProfileSerializer
from .models import CustomUser, OTP, Profile, Task
from .tasks import send_otp_email
from .mixin import RBACMixin
from .pagination import StandardResultsSetPagination
from .permissions import IsTaskOwner

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
            send_otp_email.apply_async(args=[user.id])
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

            # Verify OTP
            if int(otp.code) == otp_code:
                logger.info(f"OTP verified successfully for {email} at {now()}")
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                otp.delete()  # Invalidate OTP after successful login

                # Use RBACMixin to get the RBAC information for the user
                rbac = RBACMixin().get_feature_access_map(user=user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': 'admin' if user.is_superuser else 'user',
                    'user_id': user.id,
                    'message': f'{user.username} logged in',
                    'rbac': rbac
                }, status=status.HTTP_200_OK)

            logger.warning(f"Invalid or expired OTP for {email} at {now()}")
            return Response({'detail': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            logger.warning(f"User {email} not found during OTP verification attempt at {now()}")
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class RefreshTokenView(TokenRefreshView):
    permission_classes = [IsAuthenticated]


class ProfileViewSet(RBACMixin, viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def check_permissions(self, request):
        # Use RBAC for permission checks
        rbac_check = self.has_feature_access()
        if not rbac_check:
            self.permission_denied(
                request, 
                message='You do not have permission to perform this action.',
                code='permission_denied'
            )
        super().check_permissions(request)
    


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwner]
    
    rbac_data = {
        'page': 'tasks',
        'feature': 'task_list'
    }

    def get_queryset(self):
        return Task.objects.all().select_related('created_by', 'assignee')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def check_permissions(self, request):
        
        rbac_checker = RBACMixin(request=request, view=self)
        
        # Use RBAC for permission checks
        rbac_check = rbac_checker.has_feature_access()
        if not rbac_check:
            self.permission_denied(
                request, 
                message='You do not have permission to perform this action.',
                code='permission_denied'
            )
        super().check_permissions(request)