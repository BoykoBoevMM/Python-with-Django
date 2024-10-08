from rest_framework import serializers
from .models import Post, Tag, Comment, Vote


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'id']
        read_only_fields = ['id']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['vote_type', 'author', 'id']
        read_only_fields = ['id', 'author', 'date']
        
    def validate_vote_type(self, value):
        VALID_TYPES = (0, 1)
        try:
            value = int(value)
        except ValueError:
            raise serializers.ValidationError("Vote type must be an integer!")
        if value not in VALID_TYPES:
            raise serializers.ValidationError("Vote type should be 0 or 1!")
        return value

    def create(self, validated_data):
        # import pdb; pdb.set_trace()
        request = self.context.get('request', None)
        post_id = self.context['view'].kwargs.get('post_id')
        post = Post.objects.get(id=post_id)        
        author = request.user
        vote, created = Vote.objects.update_or_create(author=author, post=post, defaults=validated_data)
        return vote


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


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    votes = VoteSerializer(many=True, source='vote_set', read_only=True)
    comments = CommentSerializer(many=True, source='comment_set', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'link', 'tags', 'author', 'date', 'votes', 'comments']
        read_only_fields = ['id', 'author', 'date', 'votes', 'comments', 'tags']
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['tags'] = [tag.name for tag in instance.tags.all()]
    #     return representation
    
    def validate_tags(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("Hashtags limit is 10")
        return value
    
    def handle_tags(self, validated_data):
        tags = []
        for tag_name in validated_data:
            tag, created = Tag.objects.get_or_create(**tag_name)
            tags.append(tag)
        return tags

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        tags = self.handle_tags(tags_data)
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        tags = self.handle_tags(tags_data)
        instance.tags.set(tags)
        return instance



