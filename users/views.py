from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from configs.utils import set_context
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterUserView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context=set_context(request)
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


"""
class CreateTokenView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccessKeySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data={}, context=set_context(request))
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
"""