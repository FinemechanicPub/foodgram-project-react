"""Модуль вспомогательных функций"""
from django.conf import settings


def cut_text_display(text):
    """Обрезание текста при выводе на экран"""
    return text[:settings.RECIPES['TEXT_DISPLAY_LENGTH']]

