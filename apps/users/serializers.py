import base64
import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.validators import UniqueValidator
from .models import User


class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=30, read_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('LOGIN_EMAIL_REQUIRED')
        if password is None:
            raise serializers.ValidationError('LOGIN_PASSWORD_REQUIRED')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('LOGIN_EMAIL_PASSWORD_WRONG')

        if not user.check_password(password):
            raise serializers.ValidationError('LOGIN_EMAIL_PASSWORD_WRONG')

        user.last_login = timezone.now()
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt.encode(
            payload,
            base64.b64decode(settings.SECRET_KEY),
            algorithm=settings.JWT_ALGORITHM
        )
        user.token = token.decode()

        return user


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'name',
            'password',
            'is_superuser',
            'last_login',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)