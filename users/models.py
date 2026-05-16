from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.constants import MAX_LENGTH_ABOUT, MAX_LENGTH_NAME, MAX_LENGTH_PHONE, MAX_LENGTH_SURNAME
from core.validators import phone_validator, validate_github_url

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    surname = models.CharField(max_length=MAX_LENGTH_SURNAME)
    avatar = models.URLField(default='', blank=True)
    phone = models.CharField(
        validators=[phone_validator],
        max_length=MAX_LENGTH_PHONE,
        unique=True,
        blank=True,
        null=True
    )
    github_url = models.URLField(blank=True, null=True, validators=[validate_github_url])
    about = models.TextField(max_length=MAX_LENGTH_ABOUT, blank=True, default='')
    favorites = models.ManyToManyField('projects.Project', related_name='interested_users', blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def __str__(self):
        return self.email
