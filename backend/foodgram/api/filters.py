from django.db.models import OuterRef
from django_filters import rest_framework as filter

from recipes.models import Favorite, ShoppingCart, Tag


class IngredientFilter(filter.FilterSet):
    name = filter.CharFilter(lookup_expr='istartswith')


class RecipeFilter(filter.FilterSet):
    author = filter.NumberFilter(lookup_expr='exact', field_name='author__id')
    is_in_shopping_cart = filter.BooleanFilter()
    is_favorited = filter.BooleanFilter()
    tags = filter.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        to_field_name='slug',
        lookup_expr='exact',
        field_name='tags__slug'
    )


class RecipeListFilter(filter.FilterSet):

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(recipe=OuterRef('pk'), user=self.request.user)


class ShoppingCartFilter(RecipeListFilter):
    class Meta:
        model = ShoppingCart
        fields = []


class FavoritesFilter(RecipeListFilter):
    class Meta:
        model = Favorite
        fields = []
