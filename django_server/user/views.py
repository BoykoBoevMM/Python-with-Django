from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'user/home.html')
    # return HttpResponse("<h2>Home page</h2>")

def login(request):
    return render(request, 'user/login.html')
    # return HttpResponse("<h2>Login page</h2>")

def register(request):
    return render(request, 'user/register.html')
    # return HttpResponse("<h2>Register page</h2>")
