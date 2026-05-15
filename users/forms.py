from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.constants import MAX_LENGTH_NAME, MAX_LENGTH_SURNAME
from core.validators import validate_github_url
from .models import User


class RegisterForm(UserCreationForm):
    name = forms.CharField(label='Имя', max_length=MAX_LENGTH_NAME)
    surname = forms.CharField(label='Фамилия', max_length=MAX_LENGTH_SURNAME)
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    github_url = forms.URLField(
        label='GitHub',
        required=False,
        validators=[validate_github_url]
    )

    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'avatar': 'Аватар (URL)',
            'about': 'О себе',
            'phone': 'Телефон',
            'github_url': 'GitHub',
        }
