from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True, 
        required=True
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        return data

