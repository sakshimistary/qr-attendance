from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model


# Create your models here.

class User(AbstractUser):
    mobile_no = models.CharField(max_length=10, unique=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joining_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.user and Trainer.objects.filter(user=self.user).exists():
            raise ValidationError("User is already Trainer. Cannot create student for it")

    def __str__(self):
        return self.user.get_full_name()


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joining_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.user and Student.objects.filter(user=self.user).exists():
            raise ValidationError("User is already Student. Cannot create trainer for it")

    def __str__(self):
        return self.user.get_full_name()