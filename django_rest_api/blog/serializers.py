from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Post, Tag, Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        # fields = ['name', 'id']
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'
        # fields = ['title', 'content', 'link', 'tags']
        read_only_fields = ['id', 'author', 'date']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = [tag.name for tag in instance.tags.all()]
        return representation
    
    def validate_tags(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("Hashtags limit is 10")
        return value
        
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        
        post.tags.set(tags)
        return post
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        
        instance.tags.set(tags)
        
        return instance


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


