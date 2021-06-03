from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from configs.utils import set_context
from configs.permissions import StaffOnly
from .models import User
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


class ReGenerateTokenView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        request.user.generate_token()
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ('id', 'email')

    def get_queryset(self):
        return self.filter_queryset(self.queryset)

    def get_object(self, pk=None):
        try:
            return self.queryset.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound('Not Found')

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = self.get_object(pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        user = self.get_object(pk)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        user = self.get_object(pk)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)