from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Project


class RegisterForm(UserCreationForm):
    name = forms.CharField(label='Имя', max_length=124)
    surname = forms.CharField(label='Фамилия', max_length=124)
    email = forms.EmailField(label='Email')
    
    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password1', 'password2']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        labels = {
            'name': 'Название проекта',
            'description': 'Описание',
            'github_url': 'GitHub',
            'status': 'Статус',
        }
