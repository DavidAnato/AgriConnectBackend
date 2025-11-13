from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
import requests
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from .serializers import (
    RegisterSerializer, LoginSerializer, OTPVerificationSerializer,
    EmailValidateRequestSerializer, GoogleLoginSerializer, UserProfileSerializer,
    ChangePasswordSerializer, SetPasswordSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, 
)
from utils.functions import send_activation_email, generate_otp_code, send_password_reset_email

User = get_user_model()
logger = logging.getLogger(__name__)


class BaseLoginView:
    """Base class for login views with common methods"""
    
    def enrich_user_data(self, user):
        """Enrich user data with additional information"""
        return {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'verified_email': user.verified_email,
            'profile_picture': (
                user.profile_picture.url if getattr(user, "profile_picture", None) and hasattr(user.profile_picture, "url") else None
            ),
            'date_joined': user.date_joined.isoformat() if user.date_joined else None,
            'phone_number': user.phone_number,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'farm_name': user.farm_name if hasattr(user, 'farm_name') else None,
            'farm_address': user.farm_address if hasattr(user, 'farm_address') else None,
            'farm_description': user.farm_description if hasattr(user, 'farm_description') else None,
            'google_id': user.google_id,
        }


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        user.otp_code = generate_otp_code()
        user.otp_generated_at = timezone.now()
        user.save()



        logger.info("Préparation de l'email d'activation")
        logger.debug(f"FRONTEND_URL utilisé : {FRONTEND_URL}")
        logger.debug(f"Adresse email du destinataire : {email}")
        logger.debug(f"Code OTP : {otp_code}")
        logger.debug(f"URL d'activation : {activation_url}")
        logger.debug(f"EMAIL_HOST_USER (expéditeur) : {settings.EMAIL_HOST_USER}")
        logger.debug(f"EMAIL_BACKEND utilisé : {settings.EMAIL_BACKEND}")
        try:
            send_activation_email(user.email, user.otp_code)
        except Exception as e:
            raise Exception(f"Erreur lors de l'envoi de l'email : {str(e)}")

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response(
                {"message": "Inscription réussie. Vérifiez votre email pour activer votre compte."},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RendActivationView(generics.CreateAPIView):
    serializer_class = EmailValidateRequestSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response(
                    {"error": "User with this email is already activated."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Generate new OTP
        otp_code = generate_otp_code()
        user.otp_code = otp_code
        user.otp_generated_at = timezone.now()
        user.save()

        # Send email with new OTP
        try:
            send_activation_email(user.email, otp_code)
        except Exception as e:
            return Response(
                {"error": f"Failed to send email: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"message": "New OTP sent successfully."}, 
            status=status.HTTP_201_CREATED
        )


class EmailActivateView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        return self.activate_account(
            request.data.get("email"), request.data.get("otp_code")
        )

    def activate_account(self, email, otp_code):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur introuvable."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.is_active and user.verified_email:
            return Response(
                {"message": "Ce compte est déjà activé."},
                status=status.HTTP_200_OK
            )

        if user.otp_code != otp_code:
            return Response(
                {"error": "Code OTP invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérification expiration OTP (3h)
        if (
            user.otp_generated_at and 
            user.otp_generated_at + timezone.timedelta(hours=3) < timezone.now()
        ):
            return Response(
                {"error": "Le code OTP a expiré. Veuillez en demander un nouveau."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Activation du compte
        user.is_active = True
        user.verified_email = True
        user.otp_code = None
        user.otp_generated_at = None
        user.save()

        return Response(
            {"message": "Votre compte a été activé avec succès."},
            status=status.HTTP_200_OK
        )


class GoogleLoginView(BaseLoginView, generics.GenericAPIView):
    serializer_class = GoogleLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]

        # Exchange the authorization code for an access token
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        
        if token_response.status_code != 200:
            return Response(
                {"error": "Failed to exchange authorization code."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        token_json = token_response.json()
        access_token = token_json.get("access_token")

        if not access_token:
            return Response(
                {"error": "Failed to obtain access token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Use the access token to obtain user info
        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            params={"access_token": access_token},
        )
        
        if user_info_response.status_code != 200:
            return Response(
                {"error": "Failed to obtain user information."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        user_info = user_info_response.json()

        email = user_info.get("email")
        first_name = user_info.get("given_name", "")
        last_name = user_info.get("family_name", "")
        google_id = user_info.get("id")
        profile_picture = user_info.get("picture")
        verified_email = user_info.get("verified_email", False)

        if not email:
            return Response(
                {"error": "Failed to obtain user email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "google_id": google_id,
                "profile_picture": profile_picture,
                "verified_email": verified_email,
                "is_active": True,
            },
        )

        if not created:
            # Update existing user
            user.first_name = first_name or user.first_name
            user.last_name = last_name or user.last_name
            user.google_id = google_id
            user.profile_picture = profile_picture
            user.verified_email = verified_email
            user.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Enrich user data
        user_data = self.enrich_user_data(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": access_token,
                "user": user_data,
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Set new password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"detail": "Password updated successfully."}, 
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordView(generics.UpdateAPIView):
    """
    An endpoint for setting a new password without requiring the old password.
    """
    serializer_class = SetPasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Set new password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"detail": "Password set successfully."}, 
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(generics.GenericAPIView):
    """
    An endpoint for requesting a password reset via OTP.
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email_or_phone = serializer.validated_data.get("email_or_phone")
            user = None
            
            if "@" in email_or_phone:
                try:
                    user = User.objects.get(email=email_or_phone)
                except User.DoesNotExist:
                    return Response(
                        {"detail": "User with this email does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                try:
                    user = User.objects.get(phone_number=email_or_phone)
                except User.DoesNotExist:
                    return Response(
                        {"detail": "User with this phone number does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Generate OTP and send via email or SMS
            otp_code = generate_otp_code()
            user.otp_code = otp_code
            user.otp_generated_at = timezone.now()
            user.save()

            try:
                if "@" in email_or_phone:
                    send_password_reset_email(user.email, otp_code)
                else:
                    # TODO: Implement WhatsApp/SMS sending
                    # send_whatsapp_message(user.phone_number, otp_code)
                    return Response(
                        {"detail": "SMS/WhatsApp sending not implemented yet."},
                        status=status.HTTP_501_NOT_IMPLEMENTED
                    )
            except Exception as e:
                return Response(
                    {"detail": f"Failed to send OTP: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                {"detail": "OTP sent successfully."}, 
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    An endpoint for confirming a password reset via OTP.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data.get("otp_code")
            new_password = serializer.validated_data.get("new_password")
            
            try:
                user = User.objects.get(otp_code=otp_code, is_active=True)
            except User.DoesNotExist:
                return Response(
                    {"detail": "Invalid OTP."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check OTP expiration (3 hours)
            if (
                user.otp_generated_at
                and user.otp_generated_at + timezone.timedelta(hours=3) < timezone.now()
            ):
                return Response(
                    {"detail": "OTP has expired. Please request a new OTP."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Set new password
            user.set_password(new_password)
            user.otp_code = None
            user.otp_generated_at = None
            user.save()
            
            return Response(
                {"detail": "Password reset successfully."}, 
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(BaseLoginView, generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": self.enrich_user_data(user),
            },
            status=status.HTTP_200_OK,
        )

class CheckEmailExistsView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_description="Vérifie si une adresse email existe déjà",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email"],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email')
            },
        ),
        responses={
            200: openapi.Response(
                description="Email existence status",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'exists': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                    },
                )
            )
        }
    )
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email manquant"}, status=status.HTTP_400_BAD_REQUEST)

        exists = User.objects.filter(email=email).exists()
        return Response({"exists": exists}, status=status.HTTP_200_OK)

class UpdateUserView(generics.UpdateAPIView):
    """
    An endpoint for updating user information.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"detail": "User information updated successfully.", "user": serializer.data},
            status=status.HTTP_200_OK
        )
