from django.urls import path
from .views import login, register

urlpatterns = [
    path('login/', login, name='user-login'),
    path('register/', register, name='user-register'),
]
