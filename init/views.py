from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class InitView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response({'title': 'Django DRF'}, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({'title': request.data.get('title', 'None')}, status=status.HTTP_200_OK)