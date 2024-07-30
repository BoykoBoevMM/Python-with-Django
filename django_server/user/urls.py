from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import login, register, logout

urlpatterns = [
    path('login/', LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
    path('register/', register, name='user-register'),
]
