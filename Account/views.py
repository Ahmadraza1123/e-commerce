from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from .serializers import (UserSerializer,UserProfileSerializer,ResetPasswordRequestSerializer,PasswordResetConfirmSerializer)

User = get_user_model()


# ✅ REGISTER VIEWSET
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                send_mail(
                    subject='Welcome to E-Commerce Site!',
                    message='Thank you for registering with us!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print("Email send error:", e)

            return Response({
                "message": "User registered successfully!",
                "user": UserSerializer(user, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ LOGIN VIEW
class LoginView(APIView):
    """
    Custom JWT Login View
    """
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
        }, status=status.HTTP_200_OK)

# ✅ LOGOUT VIEW
class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


# ✅ PROFILE VIEW
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


# ✅ REQUEST PASSWORD RESET
class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found with this email."}, status=status.HTTP_404_NOT_FOUND)

        # Generate reset token
        token = default_token_generator.make_token(user)

        # ✅ Save token in DB
        user.reset_code = token
        user.save()

        reset_url = f"http://localhost:3000/reset-password/{token}"

        send_mail(
            subject="Password Reset Link",
            message=f"Click the link to reset your password:\n{reset_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)



class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        user = User.objects.filter(reset_code=token).first()
        if not user:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.reset_code = None
        user.save()

        return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)
