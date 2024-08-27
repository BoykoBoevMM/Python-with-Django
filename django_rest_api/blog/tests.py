import pytest
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from .models import Post


tag_data = {
    "name": "pytest"
}
post_data = {
	"title": "Title test",
	"content": "Content test",
    "tags": [tag_data]
}


POST_LIST_URL = reverse('blog-home-list')
POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': 1})


class TestBlogPostOrdering:
    def test_posts_list_ascending_order(self, client, create_posts):
        ordering = 'date'
        response = client.get(f"{POST_LIST_URL}?ordering={ordering}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
        assert response.data['results'][0]['date'] < response.data['results'][1]['date']

    def test_posts_list_descending_order(self, client, create_posts):
        ordering = '-date'
        response = client.get(f"{POST_LIST_URL}?ordering={ordering}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
        assert response.data['results'][0]['date'] > response.data['results'][1]['date']


class TestCreateBlogPost:
    def test_create_blog_post_unauthorized(self, client, db):
        response = client.post(POST_LIST_URL, post_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Post.objects.count() == 0
        assert response.data['detail'] == "Authentication credentials were not provided."

    def test_create_blog_post_validation(self, client, create_token):
        validation = ErrorDetail(
            string='This field is required.', 
            code='required'
        )
        response = client.post(POST_LIST_URL, HTTP_AUTHORIZATION=f'Token {create_token}')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Post.objects.count() == 0
        assert response.data['title'] == [validation]
        assert response.data['content'] == [validation]

    def test_create_blog_post(self, client, create_token):
        response = client.post(POST_LIST_URL, post_data, HTTP_AUTHORIZATION=f'Token {create_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1
        assert response.data['title'] == post_data['title']
        assert response.data['content'] == post_data['content']


class TestBlogPostDetails:
    def test_blog_post_detail(self, client, create_posts):
        first_post = create_posts[0]
        POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': first_post.id})
        response = client.get(POST_DETAIL_URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == post_data['title']
        assert response.data['content'] == post_data['content']

    def test_blog_post_detail_unauthorized(self, client, create_posts):
        first_post = create_posts[0]
        POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': first_post.id})
        response = client.put(POST_DETAIL_URL, post_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Post.objects.count() == 2
        assert response.data['detail'] == "Authentication credentials were not provided."

    def test_blog_post_detail_validation(self, client, create_token, create_posts):
        first_post = create_posts[0]
        POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': first_post.id})
        validation = ErrorDetail(
            string='This field is required.', 
            code='required'
        )
        response = client.put(POST_DETAIL_URL, HTTP_AUTHORIZATION=f'Token {create_token}')
        assert Post.objects.count() == 2
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] == [validation]
        assert response.data['content'] == [validation]

    def test_update_blog_post_detail(self, client, create_token, create_posts):
        first_post = create_posts[0]
        POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': first_post.id})
        response = client.put(
            POST_DETAIL_URL,
            data=json.dumps(post_data),
            content_type='application/json', 
            HTTP_AUTHORIZATION=f'Token {create_token}'
        )
        assert Post.objects.count() == 2
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == post_data['title']
        assert response.data['content'] == post_data['content']

    def test_delete_blog_post_detail_validation(self, client, create_posts):
        first_post = create_posts[0]
        POST_DETAIL_URL = reverse('blog-home-detail', kwargs={'pk': first_post.id})
        assert Post.objects.count() == 2
        response = client.delete(POST_DETAIL_URL)
        assert Post.objects.count() == 2
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
