from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
