from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
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
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.UUIDField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(_('LOGIN_EMAIL_REQUIRED'))
        if password is None:
            raise serializers.ValidationError(_('LOGIN_PASSWORD_REQUIRED'))

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('LOGIN_EMAIL_PASSWORD_WRONG'))

        if user is None:
            raise serializers.ValidationError(_('LOGIN_EMAIL_PASSWORD_WRONG'))

        if not user.check_password(password):
            raise serializers.ValidationError(_('LOGIN_EMAIL_PASSWORD_WRONG'))

        if not user.is_active:
            raise serializers.ValidationError(_('LOGIN_USER_DEACTIVATED'))

        user.last_login = timezone.now()
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'password',
            'is_active',
            'is_superuser',
            'access_token',
            'last_login',
            'created_at',
            'updated_at'
        )

