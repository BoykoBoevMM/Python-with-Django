import pytest
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from user.models import CustomUser

email ='test@test.com'
username ='testTest'
password ='1234567890'

user_register = {
    "id": 1,
    "email": email,
    "username": username,
    "password1": password,
    "password2": password
}

user = {
    "id": 1,
    "email": email,
    "username": username,
    "password": password,
}


class UserRegister(TestCase):
    url = reverse('user-register')
    validation = {
        "required": ErrorDetail(
            string='This field is required.', 
            code='required'
        ),
        "username": ErrorDetail(
            string='A user with that username already exists.', 
            code='unique'
        ),
        "email": ErrorDetail(
            string='user with this email already exists.', 
            code='unique'
        )
    } 

    @pytest.mark.django_db
    def test_user_register_validation(self):
        response = self.client.post(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert CustomUser.objects.count() == 0
        assert response.data['email'] == [self.validation["required"]]
        assert response.data['username'] == [self.validation["required"]]
        assert response.data['password1'] == [self.validation["required"]]
        assert response.data['password2'] == [self.validation["required"]]

    @pytest.mark.django_db
    def test_user_register_created(self):
        response = self.client.post(self.url, user_register)
        assert response.status_code == status.HTTP_201_CREATED
        assert CustomUser.objects.count() == 1
        assert response.data['id'] == user_register['id']
        assert response.data['username'] == user_register['username']
        assert type(response.data['token']) is str

    @pytest.mark.django_db
    def test_user_register_already_exist(self):
        CustomUser.objects.create_user(**user)    
        response = self.client.post(self.url, user_register)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert CustomUser.objects.count() == 1
        assert response.data['email'] == [self.validation["email"]]
        assert response.data['username'] == [self.validation["username"]]


class UserLogin(TestCase):
    url = reverse('user-login')
    validation = {
        "authentication_failed": ErrorDetail(
            string='Invalid username or password.',
            code='authentication_failed'
        ),
        "username": ErrorDetail(
            string='This field is required.', 
            code='required'
        ),
        "password": ErrorDetail(
            string='This field is required.', 
            code='required'
        )
    } 

    @pytest.mark.django_db
    def test_user_login_empty_data(self):
        response = self.client.post(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['username'] == [self.validation["username"]]
        assert response.data['password'] == [self.validation["password"]]

    @pytest.mark.django_db
    def test_user_login_validation(self):
        response = self.client.post(self.url, user)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == self.validation["authentication_failed"]
    
    @pytest.mark.django_db
    def test_user_login(self):
        CustomUser.objects.create_user(**user)
        response = self.client.post(self.url, user)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user["id"]
        assert response.data['username'] == user["username"]
        assert type(response.data['token']) is str


class UserLogout(TestCase):
    url = reverse('user-logout')
    
    @pytest.mark.django_db
    def test_user_logout_empty_data(self):
        validation = ErrorDetail(
            string='Authentication credentials were not provided.', 
            code='not_authenticated'
        )
        response = self.client.post(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == validation

    @pytest.mark.django_db
    def test_user_logout(self):
        response = self.client.post(reverse('user-register'), user_register)
        token = response.data["token"]
        response = self.client.post(self.url, HTTP_AUTHORIZATION=f'Token {token}')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'] == "Logged out successfully"
