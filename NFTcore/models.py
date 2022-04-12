import uuid

import blank
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .services import send




class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        password = uuid.uuid4().hex[:10]
        user.set_password(password)
        user.save()
        send(
            email,
            email,
            password
        )
        print(password)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField('email address', unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

# class FileGroup(models.Model):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=None, blank=True)
#     layer_name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.layer_name
#
# class File(models.Model):
#     fg = models.ForeignKey(to=FileGroup, on_delete=models.CASCADE, default=0)
#     file = models.FileField(upload_to='scripts/Input')


class LayerGroup(models.Model):
    title = models.CharField(max_length=255)


    def __str__(self):
        return self.title

class Image(models.Model):
    file = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])



# class CourseCard(models.Model):
#     image = models.ImageField(upload_to='card/img')
#     title = models.CharField(max_length=255)
#     description = models.CharField(max_length=255)
#     help_link = models.URLField(max_length=255, default='')
#
#
#     def __str__(self):
#         return self.title
