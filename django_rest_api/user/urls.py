from django.urls import path
# from django.contrib.auth.views import LogoutView
from .views import RegisterView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('register/', RegisterView.as_view(), name='user-register'),
    # path('logout/', LogoutView.as_view(), name='user-logout'),
    # path('profile/', profile, name='user-profile'),
]
