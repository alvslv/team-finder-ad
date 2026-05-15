"""
Тесты для приложения users.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    """
    Тесты для модели User.
    """

    def test_create_user(self):
        """
        Тест создания обычного пользователя.
        """
        user = User.objects.create_user(
            email='test@example.com',
            name='Test',
            surname='User',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        """
        Тест создания суперпользователя.
        """
        user = User.objects.create_superuser(
            email='admin@example.com',
            name='Admin',
            surname='User',
            password='adminpass123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
