from rest_framework import viewsets
from rest_framework import pagination
from recipes.models import Ingredient, Recipe, Tag

from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class TagViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    pagination_class = pagination.PageNumberPagination
