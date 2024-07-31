# Python-with-Django
### Cross-training Program: Python &amp; Django

## Django

A Django REST Framework (DRF) based project is a web application that uses Django REST Framework to create RESTful APIs. DRF is a powerful and flexible toolkit for building Web APIs in Django. It provides tools and features to easily create, manage, and consume RESTful APIs, which are essential for modern web applications that need to communicate with other services or provide data to frontend applications, mobile apps, and third-party systems.

**Key Components of a DRF-Based Project**
- Django Project: The main structure that contains all the settings and configurations for the web application.
- Django App: A component within the Django project that encapsulates related models, views, serializers, and other functionality.
- Models: Database schema definitions that represent the data structure.
- Serializers: Classes that define how model instances are converted to and from JSON or other content types.
- Views: Functions or classes that handle HTTP requests and return responses.
- URLs: URL patterns that map to views, making endpoints accessible to clients.
- Authentication and Permissions: Mechanisms to control access to the API.

**Features of Django REST Framework**
- Serialization: Converts complex data types like Django models into native Python datatypes and then to JSON, XML, or other content types.
- Authentication: Provides various authentication methods like token-based, session-based, OAuth, etc.
- Permissions: Controls who has access to different parts of the API.
- Throttling: Limits the rate of API requests to prevent abuse.
- Filtering, Searching, and Ordering: Adds capabilities to filter, search, and order API responses.
- Browsable API: Provides a web-based interface for interacting with the API, useful for testing and exploration.

**Typical Workflow of a DRF-Based Project**
- Define Models: Create Django models to represent the data schema.
- Create Serializers: Write serializers to convert model instances to JSON and vice versa.
- Create Views: Implement views to handle API requests and interact with models.
- Configure URLs: Map URLs to the views to define API endpoints.
- Add Authentication and Permissions: Implement authentication and permission classes to secure the API.
- Test API: Use tools like Postman, curl, or the browsable API to test endpoints.

## MVC (Model-View-Controller) Pattern

The MVC pattern is a widely used architectural design for building web applications. It divides an application into three interconnected components: Model, View, and Controller. This separation helps manage complexity in large applications by promoting modularity and separation of concerns.

### Components of MVC

**Model**
- Represents the data layer of the application.
- Manages the data, logic, and rules of the application.
- Interacts with the database to retrieve, save, update, or delete data.
- Example: In a blog application, a Post model might represent blog posts with fields like title, content, and author.

**View**
- Represents the presentation layer of the application.
- Displays data to the user and sends user commands to the controller.
- Consists of HTML, CSS, and JavaScript, or template files in a web application.
- Example: A template that renders a list of blog posts or a form for creating a new blog post.

**Controller**
- Acts as an intermediary between the Model and the View.
- Handles user input and updates the model and view accordingly.
- Example: A controller method that handles the request to create a new blog post, interacts with the Post model to save the data, and redirects to the post list view.
- Receives HTTP requests, processes them (possibly interacting with the model), and returns HTTP responses.

## MVC in Django

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. While Django follows the MVC pattern, it uses different terminology:

- Model: Remains the same.
- Template: Refers to the presentation layer (similar to the View in traditional MVC).
- View: Refers to the logic layer (similar to the Controller in traditional MVC).

Thus, in Django, the pattern is sometimes referred to as MTV (Model-Template-View).

## Important parts to emphasize

### Views
Django views are responsible for processing user requests and returning responses. There are two types of views in Django: function-based views (FBVs) and class-based views (CBVs).

#### Function-Based Views (FBVs)
Example of a simple function-based view:
```
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
```
#### Class-Based Views (CBVs)
Example of class-based views using Django's generic views:
```
# views.py
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
```

### Models
Django models define the structure of your database tables. Each model maps to a single table in the database.

Example of a simple Post model for a blog application:
```
# models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    def __str__(self):
        return self.title
```

### Migrations
Migrations are how Django propagates changes you make to your models (adding a field, deleting a model, etc.) into your database schema.

After defining or changing models, create migrations using:
- `python manage.py makemigrations`

Apply the migrations to update your database schema:
- `python manage.py migrate`

Example Migration File:
```
# migrations/0001_initial.py
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_auto_20210601_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_images/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
```

### ORM Queries
Django's ORM (Object-Relational Mapping) allows you to interact with your database using Python code instead of SQL.

#### Basic ORM Queries
Creating Objects
```
# Create a new post
post = Post.objects.create(title='My First Post', content='This is the content', author=user)
```

Retrieving Objects
```
# Get all posts
posts = Post.objects.all()

# Get a single post by primary key
post = Post.objects.get(pk=1)

# Get posts by a specific author
user_posts = Post.objects.filter(author=user)
```

Updating Objects
```
# Update a post
post = Post.objects.get(pk=1)
post.title = 'Updated Title'
post.save()
```

Deleting Objects
```
# Delete a post
post = Post.objects.get(pk=1)
post.delete()
```

#### Advanced ORM Queries
Querying with Lookups
```
# Get posts with titles containing 'Django'
posts = Post.objects.filter(title__icontains='Django')
```
Order By
```
# Get posts ordered by creation date
posts = Post.objects.order_by('created_at')
# Get posts ordered by creation date in descending order
posts = Post.objects.order_by('-created_at')
```

Aggregations
```
from django.db.models import Count, Avg

# Get the total number of posts
total_posts = Post.objects.count()

# Get the average length of post content
average_length = Post.objects.aggregate(Avg('content'))
```

Related Objects
```
# Get all posts by a specific author
author = User.objects.get(username='john')
posts_by_author = author.post_set.all()

# Get the author of a specific post
post = Post.objects.get(pk=1)
author_of_post = post.author
```

## Summary
- Views: Define how data is presented to the user. Use function-based views (FBVs) or class-based views (CBVs).
- Models: Define the structure of your database. Use Django models to create database tables.
- Migrations: Propagate changes to your models into your database schema using migrations.
- ORM Queries: Use Django's ORM to interact with your database using Python code.