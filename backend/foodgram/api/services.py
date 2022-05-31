"""Модуль обработки данных"""
from django.db.models import Sum, F
from recipes.models import Recipe


class ShoppingList:
    """Представление списка покупок"""
    LIST_ITEM = '{name}: {amount} {unit}'

    def __init__(self, user) -> None:
        self.user = user

    def as_queryset(self):
        return (
            Recipe.objects.filter(cart__user=self.user).values(
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

    def as_text(self):
        return ([self.LIST_ITEM.format(
                name=item['ingredient_name'],
                unit=item['unit'],
                amount=item['total_amount']
                ) for item in self.as_queryset()
        ])
