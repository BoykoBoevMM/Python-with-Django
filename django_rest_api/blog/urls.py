from django.urls import path, include
from rest_framework import routers
from . import views
 
router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='blog-home')
router.register(r'tags', views.TagViewSet, basename='post-tags')
router.register(r'posts/(?P<post_id>\d+)/vote', views.VoteView, basename='post-vote')
# router.register(r'posts/<int:post_id>/vote/', views.VoteView, name='post-vote'),
# router.register(r'tags', views.TagViewSet, basename='post-tags')

urlpatterns = [
    path('', include(router.urls)),
    # path('posts/<int:post_id>/vote/', views.VoteView.as_view(), name='post-vote'),
    path('posts/<int:post_id>/comments/', views.CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='post-comments-list'),
    path('posts/<int:post_id>/comments/<int:comment_id>/', views.CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='post-comments-detail'),

    
    # path('posts/', views.PostListCreateView.as_view(), name='blog-home'),
    # path('posts/new', PostCreateView.as_view(), name='post-create'),
    # path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
]
