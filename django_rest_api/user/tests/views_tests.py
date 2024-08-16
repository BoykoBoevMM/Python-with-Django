import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from user.models import CustomUser


@pytest.mark.django_db
def test_user_create():
  CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  assert CustomUser.objects.count() == 1
  

# @pytest.mark.django_db
# def test_user_login():
#     client = APIClient()
#     data = {
#         "username": "TestTest",
#         "email": "test@test.com",
#         "password1": "1234567890",
#         "password2": "1234567890"
#     }
#     response = client.post("/register/", data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert CustomUser.objects.count() == 1
#     assert CustomUser.objects.post() == data


# @pytest.mark.django_db
# def test_user_login():
#     client = APIClient()
    
#     data = {
#         "username": "TestTest",
#         "password": "1234567890"
#     }
    
#     response = client.post(reverse('user-login-list'), data)
    
#     assert response.status_code == status.HTTP_201_CREATED
#     assert CustomUser.objects.count() == 1
#     assert CustomUser.objects.post().title == "Test Post"
