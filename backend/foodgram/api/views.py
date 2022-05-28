from django_filters import rest_framework as filters
from rest_framework import pagination, viewsets
from recipes.models import Ingredient, Recipe, Tag

from .filters import IngredientFilter
from .pagination import RecipePagination
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class TagViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
