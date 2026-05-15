from django.db import models
from core.constants import (
    MAX_LENGTH_PROJECT_NAME,
    MAX_LENGTH_STATUS,
    STATUS_OPEN,
    STATUS_CLOSED,
    STATUS_CHOICES,
)
from core.validators import validate_github_url


class Project(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_PROJECT_NAME)
    description = models.TextField(blank=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(blank=True, null=True, validators=[validate_github_url])
    status = models.CharField(max_length=MAX_LENGTH_STATUS, choices=STATUS_CHOICES, default=STATUS_OPEN)
    participants = models.ManyToManyField('users.User', related_name='participated_projects', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
