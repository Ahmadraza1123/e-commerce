from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'role',
            'address',
            'user_profile',
        ]

    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        """Create user with hashed password."""
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'customer'),
            address=validated_data.get('address', ''),
            user_profile=validated_data.get('user_profile'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'address', 'user_profile']


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Check if user exists with that email."""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):

    token = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=6)