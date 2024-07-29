from django.shortcuts import render
from django.http import HttpResponse
import datetime

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
