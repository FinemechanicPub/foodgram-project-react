"""Вспомогательные классы и функции"""
from django.db.models import BooleanField, Exists, OuterRef, Value

from users.models import Subscription


class URLParameter():
    """Значение по умолчанию из параметров URL"""
    requires_context = True

    def __init__(self, field_name):
        self.field_name = field_name

    def __call__(self, serializer_field):
        return (
            serializer_field.context.get('request')
            .parser_context.get('kwargs').get(self.field_name)
        )


def is_subscribed_annotation(queryset, user):
    """Добавление признака подписки пользователя на автора рецепта"""
    if user.is_authenticated:
        return queryset.annotate(
            is_subscribed=Exists(
                Subscription.objects.filter(
                    subscriber=user,
                    author=OuterRef('pk')
                )
            )
        )
    else:
        return queryset.annotate(is_subscribed=Value(False, BooleanField()))
