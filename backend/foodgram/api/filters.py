from django import forms
from django_filters import rest_framework as filter
from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(filter.FilterSet):
    name = filter.CharFilter(lookup_expr='istartswith')

    class Meta:
        Model = Ingredient


class MultipleCharFilter(filter.MultipleChoiceFilter):
    field_class = forms.CharField


class RecipeFilter(filter.FilterSet):
    author = filter.NumberFilter(lookup_expr='exact', field_name='author__id')
    tags = filter.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        to_field_name='slug',
        lookup_expr='exact',
        field_name='tags__slug'
    )

    class Meta:
        Model = Recipe
