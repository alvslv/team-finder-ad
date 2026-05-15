"""
Тесты для приложения projects.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Project

User = get_user_model()


class ProjectModelTest(TestCase):
    """
    Тесты для модели Project.
    """

    def setUp(self):
        """
        Создание тестового пользователя.
        """
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test',
            surname='User',
            password='testpass123'
        )

    def test_create_project(self):
        """
        Тест создания проекта.
        """
        project = Project.objects.create(
            name='Тестовый проект',
            description='Описание тестового проекта',
            owner=self.user
        )
        self.assertEqual(project.name, 'Тестовый проект')
        self.assertEqual(project.owner, self.user)
        self.assertEqual(project.status, 'open')
