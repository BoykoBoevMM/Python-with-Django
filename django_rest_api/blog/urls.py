from django.urls import path, include
from rest_framework import routers
from . import views
 
router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='blog-home')
router.register(r'tags', views.TagViewSet, basename='post-tags')
router.register(r'posts/(?P<post_id>\d+)/vote', views.VoteView, basename='post-vote')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', views.CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='post-comments-list'),
    path('posts/<int:post_id>/comments/<int:pk>/', views.CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='post-comments-detail'),
]

urlpatterns += router.urls
