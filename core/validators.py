"""Валидаторы для полей моделей."""

import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_github_url(value):
    """Проверяет, что ссылка ведёт на GitHub."""
    if not value:
        return
    if not re.match(r'^https?://(www\.)?github\.com/[\w\-]+/?$', value):
        raise ValidationError('Ссылка должна вести на GitHub.')


phone_validator = RegexValidator(
    regex=r'^(\+7|8)?\d{10}$',
    message="Формат: +79991234567 или 89991234567"
)
