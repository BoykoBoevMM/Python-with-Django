from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
                'id': user.pk,
                'token': token.key,
                'username': user.username
            }, status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request=request,
            username=serializer.validated_data["username"], 
            password=serializer.validated_data["password"]
        )
        if not user:
            raise AuthenticationFailed("Invalid username or password.")
        token, created = Token.objects.get_or_create(user=user)
        return Response({
                'id': user.pk,
                'token': token.key,
                'username': user.username
            }, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
