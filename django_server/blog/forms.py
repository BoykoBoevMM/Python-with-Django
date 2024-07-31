from .models import Post, Comment
from django.forms import ModelForm

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
        
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'link', 'image']
        template_name = 'blog/post_form.html'