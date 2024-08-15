from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from django.contrib.auth import login
from django.contrib.auth.models import User

from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser


class RegisterView(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            userData = serializer.save()
            return Response(userData, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
