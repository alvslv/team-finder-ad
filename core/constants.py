"""Константы для всего проекта."""

from enum import StrEnum

# Длины полей для модели User
MAX_LENGTH_NAME = 124
MAX_LENGTH_SURNAME = 124
MAX_LENGTH_PHONE = 12
MAX_LENGTH_ABOUT = 256

# Длины полей для модели Project
MAX_LENGTH_PROJECT_NAME = 200
MAX_LENGTH_STATUS = 6

# Статусы проекта
STATUS_OPEN = 'open'
STATUS_CLOSED = 'closed'
STATUS_CHOICES = [
    (STATUS_OPEN, 'Открыт'),
    (STATUS_CLOSED, 'Закрыт'),
]

# Параметры аватара
DEFAULT_AVATAR_SIZE = 120

# Пагинация
PROJECTS_PER_PAGE = 12
USERS_PER_PAGE = 12

# Цвета для аватара (мягкие тона)
class AvatarColor(StrEnum):
    """Цвета для фона аватара."""
    GRAY = '4a5568'
    DARK_GRAY = '2d3748'
    DARK_BLUE = '1a365d'
    GREEN = '22543d'
    RED = '9b2c2c'
    BROWN = '744210'
    BLUE = '2c5282'
    TEAL = '285e61'


# Список цветов для случайного выбора
AVATAR_BG_COLORS = [
    AvatarColor.GRAY,
    AvatarColor.DARK_GRAY,
    AvatarColor.DARK_BLUE,
    AvatarColor.GREEN,
    AvatarColor.RED,
    AvatarColor.BROWN,
    AvatarColor.BLUE,
    AvatarColor.TEAL,
]
