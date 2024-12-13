from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import CustomUser


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return JsonResponse(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(
            username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            )
        else:
            return JsonResponse(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


