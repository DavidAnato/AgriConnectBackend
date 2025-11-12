from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User  # Changé de CustomUser à User
        fields = ("email", "first_name", "last_name", "role", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Email ou mot de passe incorrect")
        if not user.is_active:
            raise serializers.ValidationError("Ce compte est désactivé.")
        data["user"] = user
        return data

class OTPVerificationSerializer(serializers.Serializer):
    """
    Serializer for OTP verification.
    """
    otp_code = serializers.CharField(min_length=6, max_length=6)  # Changé de 5 à 6
    email = serializers.EmailField()

    def validate_otp_code(self, value):  # Changé de validate_otp à validate_otp_code
        """
        Validate the OTP code.
        """
        try:
            user = User.objects.get(
                otp_code=value, is_active=False, verified_email=False
            )
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP. Please try again.")

class EmailValidateRequestSerializer(serializers.Serializer):
    """
    Serializer for email validation request.
    """
    email = serializers.EmailField()

class GoogleLoginSerializer(serializers.Serializer):
    """
    Serializer for Google login.
    """
    code = serializers.CharField()

    def validate_code(self, value):
        """
        Validate the authorization code.
        """
        if not value:
            raise serializers.ValidationError("Authorization code is required.")
        return value

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing the password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate_old_password(self, value):
        """
        Validate the old password.
        """
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

class SetPasswordSerializer(serializers.Serializer):
    """
    Serializer for setting a new password.
    """
    new_password = serializers.CharField(required=True, min_length=8)

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    """
    email_or_phone = serializers.CharField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming the password reset.
    """
    new_password = serializers.CharField(min_length=8, write_only=True)
    otp_code = serializers.CharField(min_length=6, max_length=6)  # Changé de 5 à 6

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            'otp_code': {'write_only': True},
        }