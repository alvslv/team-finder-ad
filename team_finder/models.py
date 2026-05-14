from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

def generate_avatar(name, surname):
    """Генерирует аватар из первой буквы имени"""
    letter = name[0].upper() if name else 'U'
    return f'https://ui-avatars.com/api/?name={letter}&background=random&color=fff&size=120'

class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if not user.avatar:
            user.avatar = generate_avatar(name, surname)
            user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.URLField(default='', blank=True)
    phone_regex = RegexValidator(regex=r'^(\+7|8)?\d{10}$', message="Формат: +79991234567 или 89991234567")
    phone = models.CharField(validators=[phone_regex], max_length=12, unique=True, blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(max_length=256, blank=True, default='')
    favorites = models.ManyToManyField('Project', related_name='interested_users', blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def __str__(self):
        return self.email

class Project(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыт'),
        ('closed', 'Закрыт'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='open')
    participants = models.ManyToManyField(User, related_name='participated_projects', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
