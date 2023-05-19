from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

# Create your models here.


class blog(models.Model):
    id = models.BigAutoField(primary_key=True)
    artical = models.CharField(max_length=1500)
    title = models.CharField(max_length=200, default='')
    slug = AutoSlugField(populate_from="title", max_length=200, unique=True)

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    is_verified = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now=True)
    token = models.CharField(null=True, blank=True, max_length=50)
    