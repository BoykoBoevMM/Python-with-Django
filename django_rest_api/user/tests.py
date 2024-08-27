import pytest
from django.urls import reverse
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


class TestUserRegister:
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

    def test_user_register_validation(self, client, db):
        response = client.post(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert CustomUser.objects.count() == 0
        assert response.data['email'] == [self.validation["required"]]
        assert response.data['username'] == [self.validation["required"]]
        assert response.data['password1'] == [self.validation["required"]]
        assert response.data['password2'] == [self.validation["required"]]

    def test_user_register_created(self, client, db):
        response = client.post(self.url, user_register)
        assert response.status_code == status.HTTP_201_CREATED
        assert CustomUser.objects.count() == 1
        assert response.data['id'] == user_register['id']
        assert response.data['username'] == user_register['username']
        assert type(response.data['token']) is str

    def test_user_register_already_exist(self, client, db):
        CustomUser.objects.create_user(**user)    
        response = client.post(self.url, user_register)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert CustomUser.objects.count() == 1
        assert response.data['email'] == [self.validation["email"]]
        assert response.data['username'] == [self.validation["username"]]


class TestUserLogin:
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

    def test_user_login_empty_data(self, client, db):
        response = client.post(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['username'] == [self.validation["username"]]
        assert response.data['password'] == [self.validation["password"]]

    def test_user_login_validation(self, client, db):
        response = client.post(self.url, user)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == self.validation["authentication_failed"]
    
    def test_user_login(self, client, db):
        CustomUser.objects.create_user(**user)
        response = client.post(self.url, user)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user["id"]
        assert response.data['username'] == user["username"]
        assert type(response.data['token']) is str


class TestUserLogout:
    url = reverse('user-logout')
    
    def test_user_logout_empty_data(self, client, db):
        validation = ErrorDetail(
            string='Authentication credentials were not provided.', 
            code='not_authenticated'
        )
        response = client.post(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == validation

    def test_user_logout(self, client, db, create_token):
        response = client.post(self.url, HTTP_AUTHORIZATION=f'Token {create_token}')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'] == "Logged out successfully"
