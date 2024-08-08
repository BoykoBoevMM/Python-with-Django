from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Post, Tag, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
