# Django Migrations and Database


### `makemigrations`
```
C:\Boyko Boev\Python-with-Django\django_server (main -> origin)
λ python manage.py makemigrations
Migrations for 'user':
  user\migrations\0001_initial.py
    - Create model Post
```

### `migrate`
```
C:\Boyko Boev\Python-with-Django\django_server (main -> origin)
λ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, user
Running migrations:
  Applying user.0001_initial... OK
```

### `shell` ( Get user data )
```
C:\Boyko Boev\Python-with-Django\django_server (main -> origin)
λ python manage.py shell
Python 3.11.8 (tags/v3.11.8:db85d51, Feb  6 2024, 22:03:32) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from user.models import Post
>>> from django.contrib.auth.models import User
>>> User.objects.all()
<QuerySet [<User: BoykoBoev>, <User: TestAdmin>]>
>>> User.objects.first()
<User: BoykoBoev>
>>> User.objects.last()
<User: TestAdmin>
>>> User.objects.filter(username='BoykoBoev')
<QuerySet [<User: BoykoBoev>]>
>>> User.objects.filter(username='BoykoBoev').first()
<User: BoykoBoev>
>>> user = User.objects.filter(username='BoykoBoev').first()
>>> user
<User: BoykoBoev>
>>> user.username
'BoykoBoev'
>>> user.email
'boyko.boev@mentormate.com'
>>> user.id
1
```

### `shell` ( Create first post )
```
>>> Post.objects.all()
<QuerySet []>
>>> post_1 = Post(title-'Blog_1', content='First post content', author=user)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'title' is not defined
>>> post_1 = Post(title='Blog_1', content='First post content', author=user)
>>> post_1.save()
>>> Post.objects.all()
<QuerySet [<Post: Post object (1)>]>
>>> q()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'q' is not defined
>>> quit()
```


### `shell` ( Create second post )
```
C:\Boyko Boev\Python-with-Django\django_server (main -> origin)
λ python manage.py shell
Python 3.11.8 (tags/v3.11.8:db85d51, Feb  6 2024, 22:03:32) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from user.models import Post
>>> from django.contrib.auth.models import User
>>> Post.objects.all()
<QuerySet [<Post: Blog_1>]>
>>> user = User.objects.filter(username='BoykoBoev').first()
>>> user.id
1
>>> user.email
'boyko.boev@mentormate.com'
>>> post_2 = Post(title='Blog 2', content='Second post content', author_id=user.id)
>>> post_2.save()
>>> Post.objects.all()
<QuerySet [<Post: Blog_1>, <Post: Blog 2>]>
>>> user.post_set
<django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x000001D8FDC23910>
>>> user.post_set.all()
<QuerySet [<Post: Blog_1>, <Post: Blog 2>]>
>>>
```

### `shell` ( Create third post )
```
>>> user.post_set.all()
<QuerySet [<Post: Blog_1>, <Post: Blog 2>]>
>>>
>>> user.post_set.create(title='Blog 3', content='Third post content')
<Post: Blog 3>
>>> Post.objects.all()
<QuerySet [<Post: Blog_1>, <Post: Blog 2>, <Post: Blog 3>]>
>>>
```