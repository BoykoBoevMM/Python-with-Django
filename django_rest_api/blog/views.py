from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from rest_framework import generics, viewsets

from .models import Tag, Post, Comment
from .forms import PostForm, CommentForm
from .serializers import PostSerializer, CommentSerializer, TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        blog_post_id = self.kwargs['post_id']
        return Comment.objects.filter(post=blog_post_id)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)
#     # return HttpResponse("<h2>Home page</h2>")
    
# class PostListView(ListView):
#     model = Post
#     tags = Tag
#     template_name = 'blog/home.html'
#     context_object_name = 'posts'
#     ordering = ['-date']

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         selected_tag = self.request.GET.get('tag')
#         if selected_tag:
#             context['posts'] = Post.objects.filter(tags__name__in=[selected_tag])
#         else:
#             context['posts'] = Post.objects.all()
#         context['tags'] = Tag.objects.all()
#         return context
    
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         tag_name = self.request.GET.get('tag')
#         if tag_name:
#             queryset = queryset.filter(tags__name=tag_name)
#         return queryset
    

# class PostDetailView(DetailView):
#     model = Post
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         context['comment_form'] = CommentForm()
#         comments = Comment.objects.filter(post=post).order_by('-date')
#         context['comments'] = comments
#         return context
    
#     def form_valid(self, form):
#         post = self.get_object()
#         form.instance.post = post
#         form.instance.author = self.request.user
#         return super().form_valid(form)
    
#     def post(self, request, *args, **kwargs):
#         form = CommentForm(request.POST)
#         post = self.get_object()
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = self.request.user
#             comment.save()
#             return redirect('post-detail', pk=post.id)
        

# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = PostForm

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
    

# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Post
#     form_class = PostForm

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
    
#     def test_func(self) -> bool | None:
#         post = self.get_object()
#         return self.request.user == post.author
    

# class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Post
#     template_name = 'blog/post_delete.html'
#     success_url = "/"

#     def test_func(self) -> bool | None:
#         post = self.get_object()
#         return self.request.user == post.author
