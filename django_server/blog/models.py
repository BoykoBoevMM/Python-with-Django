from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
# from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # tags = TaggableManager() 
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(null=True)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    # likes = models.ManyToManyField(User)

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
