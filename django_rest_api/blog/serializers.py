from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Post, Tag, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        # fields = ['title', 'content', 'link', 'tags']
        read_only_fields = ['id', 'author', 'date']
        
    def create(self, validated_data):
        request = self.context.get('request', None)
        post = Post.objects.create(author=request.user, **validated_data)
        return post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields = ['content']
        fields = '__all__'
        read_only_fields = ['id', 'author', 'date', 'post']
    
    def create(self, validated_data):
        request = self.context.get('request', None)
        comment = Comment.objects.create(author=request.user, **validated_data)
        return comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
