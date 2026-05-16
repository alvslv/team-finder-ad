from django import forms

from core.constants import MAX_LENGTH_PROJECT_NAME
from core.validators import validate_github_url

from .models import Project


class ProjectForm(forms.ModelForm):
    github_url = forms.URLField(
        label='GitHub',
        required=False,
        validators=[validate_github_url]
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        labels = {
            'name': 'Название проекта',
            'description': 'Описание',
            'github_url': 'GitHub',
            'status': 'Статус',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
