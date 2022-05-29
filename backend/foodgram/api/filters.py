from django_filters import rest_framework as filter
from recipes.models import Ingredient, Recipe


class IngredientFilter(filter.FilterSet):
    name = filter.CharFilter(lookup_expr='istartswith')

    class Meta:
        Model = Ingredient


class RecipeFilter(filter.FilterSet):
    author = filter.NumberFilter(lookup_expr='exact', field_name='author__id')

    class Meta:
        Model = Recipe
