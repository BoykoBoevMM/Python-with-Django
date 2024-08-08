from django.urls import path, include
from rest_framework import routers
from . import views
# from .views import
 
router = routers.DefaultRouter()
router.register(r'posts', views.PostListCreateViewSet, basename='blog-home')
 
urlpatterns = [
    path('', include(router.urls)),
    # path('posts/', views.PostListCreateView.as_view(), name='blog-home'),
    # path('posts/new', PostCreateView.as_view(), name='post-create'),
    # path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
]
