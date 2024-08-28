import pytest
from datetime import datetime
from django.utils import timezone
from blog.models import Post, Tag
from user.models import CustomUser
from rest_framework.authtoken.models import Token


@pytest.fixture
def create_user(db):
    return CustomUser.objects.create_user(
        id=1,
        email='test@test.com',
        username='TestTest',
        password='1234567890',
    )


@pytest.fixture
def create_token(db, create_user):
    token, created = Token.objects.get_or_create(user=create_user)
    return token


@pytest.fixture
def create_posts(db, create_user):
    tag_data = {
        "name": "pytest"
    }
    post_data = {
    	"title": "Title test",
    	"content": "Content test",
        "tags": [tag_data]
    }
    post1 = Post.objects.create(
        title=post_data['title'], 
        content=post_data['content'], 
        author=create_user,
        date=timezone.make_aware(datetime(2024, 1, 1))
    )
    post2 = Post.objects.create(
        title=post_data['title'], 
        content=post_data['content'], 
        author=create_user,
        date=timezone.make_aware(datetime(2024, 2, 2))
    )
    tag = Tag.objects.create(**tag_data)
    post1.tags.set([tag])
    return Post.objects.all()