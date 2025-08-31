from django.contrib.auth import get_user_model
from rest_framework import serializers
from .services import UserService

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'full_name')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.get('email')
        full_name = validated_data.get('full_name', '')
        
        # Use service layer instead of direct model access
        user = UserService.create_user(
            email=email,
            password=password,
            full_name=full_name
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name')


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8)