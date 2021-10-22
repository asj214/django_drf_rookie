import jwt
import base64
from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework_jwt.settings import api_settings
from apps.users.models import User


AUTH_HEADER_PREFIX = ['Bearer']

class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix not in AUTH_HEADER_PREFIX:
            return None

        user = None

        if prefix.lower() == 'Bearer'.lower():
            user = self.deserialize_jwt(token)

        if user is None:
            raise exceptions.AuthenticationFailed('No user matching this token was found.')

        return user, token

    def deserialize_jwt(self, token):
        try:
            payload = jwt.decode(token, base64.b64decode(settings.SECRET_KEY), algorithms=settings.JWT_ALGORITHM)
        except:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')

        pk = payload.get('user_id', None)
        user = User.objects.get(pk=pk)

        return user
