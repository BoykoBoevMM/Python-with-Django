from django.urls import path
from rest_framework import routers
from .views import RegisterView, LoginView


router = routers.DefaultRouter()
router.register(r'login', LoginView, basename='user-login')
router.register(r'register', RegisterView, basename='user-register')

urlpatterns = [
    # path('login/', LoginView.as_view(), name='user-login', basename='user-login'),
    # path('register/', RegisterView.as_view(), name='user-register', basename='user-register'),
    # path('logout/', LogoutView.as_view(), name='user-logout'),
]

urlpatterns += router.urls
