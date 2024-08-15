from django import forms
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from .models import CustomUser  



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    # class Meta:
    #     model = CustomUser
    #     fields = ['username', 'password']
    
    def validate(self, data):
        
        print(data)

        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        
        user = authenticate(username=username, password=password)
        if user:
            data['user'] = user
        else:
            raise serializers.ValidationError("Invalid credentials.")
        
        return data


    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return {
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        }


class RegisterSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
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

    # def validate(self, data):
    #     if data['password'] != data['password2']:
    #         raise serializers.ValidationError({"password": "Passwords must match."})
    #     return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        return user
