from django.db.models import OuterRef, Exists, Value, IntegerField
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import pagination, viewsets, decorators, exceptions, response, status
from recipes.models import Ingredient, Recipe, ShoppingCart, Tag

from .filters import IngredientFilter, RecipeFilter
from .pagination import RecipePagination
from .serializers import FavoritesSerializer, IngredientSerializer, RecipeSerializer, RecipeShortSerializer, ShoppingCartSerialzier, TagSerializer


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

    def _recipe_list_action(self, request, pk, SerializerClass):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            list_serializer = SerializerClass(
                data=request.data,
                context={'request': request}
            )
            list_serializer.is_valid(raise_exception=True)
            list_serializer.save(user=request.user, recipe=recipe)
            recipe_serializer = RecipeShortSerializer(recipe)
            headers = self.get_success_headers(recipe_serializer.data)
            return response.Response(
                recipe_serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        elif request.method == 'DELETE':
            ShoppingCart.objects.filter(
                user=request.user,
                recipe=recipe
            ).delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        raise exceptions.MethodNotAllowed(request.method)

    @decorators.action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk=None):        
        return self._recipe_list_action(
            request,
            pk,
            ShoppingCartSerialzier
        )
    
    @decorators.action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk=None):        
        return self._recipe_list_action(
            request,
            pk,
            FavoritesSerializer
        )
        
