from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from rest_framework import generics, viewsets, permissions, mixins, filters
from rest_framework.pagination import PageNumberPagination

from .models import Tag, Post, Comment, Vote
from .forms import PostForm, CommentForm
from .serializers import PostSerializer, CommentSerializer, TagSerializer, VoteSerializer
from .guards import IsAuthenticated, IsCreator, IsAdmin, IsAdminOrIsCreator
from .pagination import HashtagsPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    
    def get_permissions(self):        
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrIsCreator()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def get_queryset(self):
        order_by = '-date'
        order = self.request.query_params.get('order')
        if order == 'asc':
            order_by = 'date'
 
        queryset = self.queryset.order_by(order_by)
 
        hashtag = self.request.query_params.get('hashtag')
        if hashtag is not None:
            queryset = queryset.filter(tags=hashtag)
 
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):        
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrIsCreator()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(post=post)
    
    def get_queryset(self):
        blog_post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=blog_post_id)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = HashtagsPagination
    permission_classes = [IsAdmin]


class VoteView(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):        
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsCreator()]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        # import pdb; pdb.set_trace()
        serializer.save(post=post, author=user)
