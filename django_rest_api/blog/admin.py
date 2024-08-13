from django.contrib import admin
from .models import Tag, Post, Comment, Vote

admin.site.register(Tag)
admin.site.register(Vote)
admin.site.register(Post)
admin.site.register(Comment)
