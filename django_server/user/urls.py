from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user-home'),
    path('login/', views.login, name='user-login'),
    path('register/', views.register, name='user-register'),
]
