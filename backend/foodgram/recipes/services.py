"""Модуль обработки данных"""
from django.db.models import F, Sum

from .models import Recipe


def get_shopping_list(user):
    return tuple(
        Recipe.objects.filter(cart__user=user).values(
            ingredient_name=F(
                'recipe_to_ingredients__ingredient__name'
            ),
            unit=F(
                'recipe_to_ingredients__ingredient'
                '__measurement_unit__notation'
            )
        ).annotate(
            total_amount=Sum('recipe_to_ingredients__amount')
        ).order_by('-total_amount')
    )
