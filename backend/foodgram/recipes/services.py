"""Модуль обработки данных"""
from django.db.models import Sum, F
from django.core.files.base import ContentFile
from .models import Recipe


class ShoppingList:
    """Представление списка покупок"""
    LIST_ITEM = '- {name}: {amount} {unit}'
    LIST = """
           Ваш список покупок

Для этих рецептов

{recipes}

понадобятся следующие ингредиенты:

{ingredients}
           """

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

    def _get_recipes(self):
        return Recipe.objects.filter(cart__user=self.user)

    def _get_ingredient_totals(self, recipes):
        return (
            recipes.values(
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

    
    def as_txt(self, filename):
        recipes = self._get_recipes()
        recipe_text = ', '.join(f'"{recipe.name}"' for recipe in recipes)
        ingredient_text = '\n'.join(
            self.LIST_ITEM.format(
                name =item['ingredient_name'],
                unit=item['unit'],
                amount=item['total_amount']
            ) for item in self._get_ingredient_totals(recipes)
        )        
        return ContentFile(
            self.LIST.format(
                recipes=recipe_text,
                ingredients=ingredient_text
            ).encode(encoding='utf-8'),
            f'{filename}.txt'
        )
