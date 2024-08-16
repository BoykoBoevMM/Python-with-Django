import pytest
from django.urls import reverse
from rest_framework import status
from user.models import CustomUser


@pytest.mark.django_db
def test_user_create():
  CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  assert CustomUser.objects.count() == 1
  

@pytest.mark.django_db
def test_user_register(client):
    data = {
        "username": "TestTest",
        "email": "test@test.com",
        "password1": "1234567890",
        "password2": "1234567890"
    }
    url = reverse('user-register-list')
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert CustomUser.objects.count() == 1
    assert response.data['email'] == data['email']


@pytest.mark.django_db
def test_user_login(client):
    email = 'test@test.com'
    username = 'testTest'
    password = '1234567890'
    CustomUser.objects.create_user(username, email, password)
    data = {
        "username": username,
        "password": password
    }
    url = reverse('user-login-list')
    response = client.post(url, data)
    print(response)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == email
    assert response.data['username'] == username
