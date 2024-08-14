from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(null=True)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.content


class Vote(models.Model):
    vote_type = models.CharField(max_length=2)
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.vote_type
