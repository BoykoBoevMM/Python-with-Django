from django.test import TestCase
from django.urls import reverse
from .models import User, Tag, Post
# Create your tests here.

class PostListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.tag = Tag.objects.create(name='Django')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.post.tags.add(self.tag)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')


class PostCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.tag = Tag.objects.create(name='Django')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.post.tags.add(self.tag)
        
    def test_login_guard(self):
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.tag = Tag.objects.create(name='Django')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.post.tags.add(self.tag)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')


class PostDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.tag = Tag.objects.create(name='Django')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.post.tags.add(self.tag)

    def test_login_guard(self):
        response = self.client.get(reverse('post-delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post-delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_delete.html')


class PostUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.tag = Tag.objects.create(name='Django')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.post.tags.add(self.tag)

    def test_login_guard(self):
        response = self.client.get(reverse('post-update', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        
    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post-update', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')
