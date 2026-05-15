"""Вспомогательные функции для проекта."""

import random
from core.constants import DEFAULT_AVATAR_SIZE, AVATAR_BG_COLORS


def generate_avatar(name, surname):
    """
    Генерирует URL аватара из первой буквы имени.
    Цвет фона выбирается случайным образом из предустановленных мягких цветов.
    """
    letter = name[0].upper() if name else 'U'
    bg_color = random.choice(AVATAR_BG_COLORS)
    return f'https://ui-avatars.com/api/?name={letter}&background={bg_color}&color=fff&size={DEFAULT_AVATAR_SIZE}'
