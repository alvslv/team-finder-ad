"""Константы для всего проекта."""

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

# Длины полей
MAX_LENGTH_NAME = 124
MAX_LENGTH_SURNAME = 124
MAX_LENGTH_PROJECT_NAME = 200

# Параметры аватара
DEFAULT_AVATAR_SIZE = 120
AVATAR_BG_COLORS = [
    '4a5568', '2d3748', '1a365d', '22543d', '9b2c2c', '744210', '2c5282', '285e61'
]
