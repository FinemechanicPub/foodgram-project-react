from django.db.models import OuterRef, Exists, Value, IntegerField
from django_filters import rest_framework as filters
from rest_framework import pagination, viewsets
from recipes.models import Ingredient, Recipe, ShoppingCart, Tag

from .filters import IngredientFilter, RecipeFilter
from .pagination import RecipePagination
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class TagViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = (
        Recipe.objects.all()
        .select_related('author')
        .prefetch_related('tags')
        .prefetch_related(
            'recipe_to_ingredients__ingredient__measurement_unit'
        )
    )
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.annotate(is_in_shopping_cart=Exists(
                ShoppingCart.objects.filter(
                    recipe=OuterRef('pk'),
                    user=self.request.user
                )
            ))
        return self.queryset.annotate(
            is_in_shopping_cart=Value(0, IntegerField())
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
