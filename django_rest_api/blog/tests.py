import pytest
import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from .models import Post, Tag
from user.models import CustomUser
from datetime import datetime


email ='test@test.com'
username ='TestTest'
password ='1234567890'
user_data = {
    "id": 1,
    "email": email,
    "username": username,
    "password": password,
}
tag_data = {
    "name": "pytest"
}
post_data = {
	"title": "Title test",
	"content": "Content test",
    "tags": [tag_data]
}

@pytest.fixture
def user():
    return CustomUser.objects.create_user(**user_data)

def login_user(client):
    response = client.post(reverse('user-login'), user_data)
    token = response.data["token"]
    return token


@pytest.fixture
def post():
    user_data = CustomUser.objects.get(
        username=username, 
        email=email
    )
    post1 = Post.objects.create(
        title=post_data['title'], 
        content=post_data['content'], 
        author=user_data,
        date=timezone.make_aware(datetime(2024, 1, 1))
    )
    post2 = Post.objects.create(
        title=post_data['title'], 
        content=post_data['content'], 
        author=user_data,
        date=timezone.make_aware(datetime(2024, 2, 2))
    )
    tag = Tag.objects.create(**tag_data)
    post1.tags.set([tag])
    return [post1, post2]


POST_LIST_URL = reverse('blog-home-list')
POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': 1})


class TestBlogPostOrdering:
    @pytest.mark.django_db
    def test_posts_list_ascending_order(self, client, user, post):
        ordering = 'date'
        response = client.get(f"{POST_LIST_URL}?ordering={ordering}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
        assert response.data['results'][0]['date'] < response.data['results'][1]['date']

    @pytest.mark.django_db
    def test_posts_list_descending_order(self, client, user, post):
        ordering = '-date'
        response = client.get(f"{POST_LIST_URL}?ordering={ordering}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
        assert response.data['results'][0]['date'] > response.data['results'][1]['date']


class TestCreateBlogPost:
    @pytest.mark.django_db
    def test_create_blog_post_unauthorized(self, client, user, post):
        response = client.post(POST_LIST_URL, post_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Post.objects.count() == 2
        assert response.data['detail'] == "Authentication credentials were not provided."

    @pytest.mark.django_db
    def test_create_blog_post_validation(self, client, user, post):
        validation = ErrorDetail(
            string='This field is required.', 
            code='required'
        )
        token = login_user(client)
        response = client.post(POST_LIST_URL, HTTP_AUTHORIZATION=f'Token {token}')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Post.objects.count() == 2
        assert response.data['title'] == [validation]
        assert response.data['content'] == [validation]

    @pytest.mark.django_db
    def test_create_blog_post(self, client, user):
        token = login_user(client)
        response = client.post(POST_LIST_URL, post_data, HTTP_AUTHORIZATION=f'Token {token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1
        assert response.data['title'] == post_data['title']
        assert response.data['content'] == post_data['content']


class TestBlogPostDetails:
    @pytest.mark.django_db
    def test_blog_post_detail(self, client, user, post):
        first_post = Post.objects.first()
        POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': first_post.id})
        response = client.get(POST_DETAIL_URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == post_data['title']
        assert response.data['content'] == post_data['content']

    @pytest.mark.django_db
    def test_blog_post_detail_unauthorized(self, client, user, post):
        first_post = Post.objects.first()
        POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': first_post.id})
        response = client.put(POST_DETAIL_URL, post_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Post.objects.count() == 2
        assert response.data['detail'] == "Authentication credentials were not provided."

    @pytest.mark.django_db
    def test_blog_post_detail_validation(self, client, user, post):
        first_post = Post.objects.first()
        POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': first_post.id})
        validation = ErrorDetail(
            string='This field is required.', 
            code='required'
        )
        token = login_user(client)
        response = client.put(POST_DETAIL_URL, HTTP_AUTHORIZATION=f'Token {token}')
        assert Post.objects.count() == 2
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] == [validation]
        assert response.data['content'] == [validation]

    @pytest.mark.django_db
    def test_update_blog_post_detail(self, client, user, post):
        first_post = Post.objects.first()
        POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': first_post.id})
        token = login_user(client)
        response = client.put(
            POST_DETAIL_URL,
            data=json.dumps(post_data),
            content_type='application/json', 
            HTTP_AUTHORIZATION=f'Token {token}'
        )
        assert Post.objects.count() == 2
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == post_data['title']
        assert response.data['content'] == post_data['content']

    @pytest.mark.django_db
    def test_delete_blog_post_detail_validation(self, client, user, post):
        first_post = Post.objects.first()
        POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': first_post.id})
        assert Post.objects.count() == 2
        response = client.delete(POST_DETAIL_URL)
        assert Post.objects.count() == 2
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
