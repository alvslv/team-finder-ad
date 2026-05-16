"""
Тесты для приложения core.
"""

from django.test import TestCase

from core.constants import (
    MAX_LENGTH_ABOUT,
    MAX_LENGTH_NAME,
    MAX_LENGTH_PHONE,
    MAX_LENGTH_PROJECT_NAME,
    MAX_LENGTH_SURNAME,
    PROJECTS_PER_PAGE,
    STATUS_CHOICES,
    STATUS_CLOSED,
    STATUS_OPEN,
    USERS_PER_PAGE,
)
from core.services import generate_avatar
from core.validators import phone_validator, validate_github_url


class ConstantsTest(TestCase):
    """
    Тесты для констант.
    """

    def test_constants_values(self):
        """
        Проверка значений констант.
        """
        self.assertEqual(MAX_LENGTH_NAME, 124)
        self.assertEqual(MAX_LENGTH_SURNAME, 124)
        self.assertEqual(MAX_LENGTH_PHONE, 12)
        self.assertEqual(MAX_LENGTH_ABOUT, 256)
        self.assertEqual(MAX_LENGTH_PROJECT_NAME, 200)
        self.assertEqual(STATUS_OPEN, 'open')
        self.assertEqual(STATUS_CLOSED, 'closed')
        self.assertEqual(len(STATUS_CHOICES), 2)
        self.assertEqual(PROJECTS_PER_PAGE, 12)
        self.assertEqual(USERS_PER_PAGE, 12)


class ValidatorsTest(TestCase):
    """
    Тесты для валидаторов.
    """

    def test_phone_validator(self):
        """
        Проверка валидатора телефона.
        """
        try:
            phone_validator('+79991234567')
        except Exception as e:
            self.fail(f"Валидатор вызвал исключение: {e}")

    def test_github_validator_correct(self):
        """
        Проверка правильной ссылки на GitHub.
        """
        try:
            validate_github_url('https://github.com/username')
        except Exception as e:
            self.fail(f"Валидатор вызвал исключение: {e}")


class ServicesTest(TestCase):
    """
    Тесты для вспомогательных функций.
    """

    def test_generate_avatar(self):
        """
        Проверка генерации аватара.
        """
        url = generate_avatar('Иван', 'Петров')
        self.assertTrue(url.startswith('https://ui-avatars.com/api/'))
        self.assertIn('name=И', url)
