from django_filters import rest_framework as filter
from recipes.models import Ingredient


class IngredientFilter(filter.FilterSet):
    name = filter.CharFilter(lookup_expr='istartswith')

    class Meta:
        Model = Ingredient