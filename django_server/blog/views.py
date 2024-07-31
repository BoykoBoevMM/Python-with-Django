from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from .forms import CommentForm
import datetime


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)
    # return HttpResponse("<h2>Home page</h2>")
    
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date']
    

class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        
        post = self.get_object()
        comments = Comment.objects.filter(post=post).order_by('-date')
        context['comments'] = comments
        
        return context
    
    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     form.instance.post = self.request.post
    #     return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post = self.get_object()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = self.request.user
            comment.save()
            return redirect('post-detail', pk=post.id)
        

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self) -> bool | None:
        post = self.get_object()
        return self.request.user == post.author
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = "/"

    def test_func(self) -> bool | None:
        post = self.get_object()
        return self.request.user == post.author
