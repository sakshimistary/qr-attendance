from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    mobile_no = models.CharField(max_length=10, unique=True)