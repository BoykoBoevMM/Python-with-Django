from django.shortcuts import render
from django.http import HttpResponse
import datetime


def home(request):
    posts = [
        {
            'author': 'Author Name',
            'title': 'First Blog Post',
            'content': 'First post content',
            'date': datetime.date.today(),
        }, {
            'author': 'Author Name',
            'title': 'First Blog Post',
            'content': 'First post content',
            'date': datetime.date.today(),
        }
    ]
    context = {
        'posts': posts
    }
    return render(request, 'user/home.html', context)
    # return HttpResponse("<h2>Home page</h2>")

def login(request):
    context = {
        'title': 'Login' 
    }
    return render(request, 'user/login.html', context)
    # return HttpResponse("<h2>Login page</h2>")

def register(request):
    context = {
        'title': 'Register' 
    }
    return render(request, 'user/register.html', context)
    # return HttpResponse("<h2>Register page</h2>")
