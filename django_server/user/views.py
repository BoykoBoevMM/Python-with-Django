from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def login(request):
    context = {
        'title': 'Login' 
    }
    return render(request, 'user/login.html', context)
    # return HttpResponse("<h2>Login page</h2>")

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
            
    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'user/register.html', context)
    # return HttpResponse("<h2>Register page</h2>")
    
def logout(request):
    return render(request, 'user/logout.html')

@login_required
def profile(request):
    return render(request, 'user/profile.html')
