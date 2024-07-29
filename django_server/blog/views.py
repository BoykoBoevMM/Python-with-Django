from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
import datetime


def home(request):
    # posts = [
    #     {
    #         'author': 'Author Name',
    #         'title': 'First Blog Post',
    #         'content': 'First post content',
    #         'date': datetime.date.today(),
    #     }, {
    #         'author': 'Author Name',
    #         'title': 'First Blog Post',
    #         'content': 'First post content',
    #         'date': datetime.date.today(),
    #     }
    # ]
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)
    # return HttpResponse("<h2>Home page</h2>")

