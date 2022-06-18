from django.contrib.auth import get_user_model
from django.db.models import (BooleanField, Count, Exists, OuterRef, Prefetch,
                              Value)
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from djoser.views import UserViewSet
from rest_framework import decorators, exceptions, response, status, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from recipes.services import get_shopping_list
from users.models import Subscription
from .filters import IngredientFilter, RecipeFilter
from .pagination import RecipePagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoritesSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeShortSerializer,
                          ShoppingCartSerialzier, SubscriptionSerializer,
                          TagSerializer, UserRecipeSerializer)
from .services import render_txt
from .utils import is_subscribed_annotation, recipe_list

User = get_user_model()


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
        .prefetch_related('tags')
        .prefetch_related(
            'recipe_to_ingredients__ingredient__measurement_unit'
        )
    )
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )

    def get_queryset(self):

        user = self.request.user
        queryset = self.queryset.prefetch_related(Prefetch(
            'author',
            is_subscribed_annotation(User.objects.all(), user)
        ))
        if user.is_authenticated:
            return queryset.annotate(
                is_in_shopping_cart=Exists(recipe_list(ShoppingCart, user)),
                is_favorited=Exists(recipe_list(Favorite, user))
            )
        return queryset.annotate(
            is_in_shopping_cart=Value(0, BooleanField()),
            is_favorited=Value(0, BooleanField())
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def _recipe_list_action(self, request, pk, serializer_class):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            list_serializer = serializer_class(
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
            serializer_class.Meta.model.objects.filter(
                user=request.user,
                recipe=recipe
            ).delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        raise exceptions.MethodNotAllowed(request.method)

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        return self._recipe_list_action(
            request,
            pk,
            ShoppingCartSerialzier
        )

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        return self._recipe_list_action(
            request,
            pk,
            FavoritesSerializer
        )

    @decorators.action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        shopping_list = get_shopping_list(request.user)
        return FileResponse(render_txt(
            shopping_list, 'my_shopping_list'),
            as_attachment=True,
        )


class WebUserViewSet(UserViewSet):

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset().annotate(
                is_subscribed=Exists(
                    Subscription.objects.filter(
                        subscriber=self.request.user,
                        author=OuterRef('pk')
                    )
                )
            )
        else:
            return super().get_queryset().annotate(
                is_subscribed=Value(False, BooleanField())
            )

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id=None):
        user = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(subscriber=request.user, author=user)
            user_serializer = UserRecipeSerializer(
                user, context={'request': request}
            )
            return response.Response(
                user_serializer.data, status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            Subscription.objects.filter(
                subscriber=request.user, author=user
            ).delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        raise exceptions.MethodNotAllowed(request.method)


class SubscriptionsViewSet(viewsets.mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = UserRecipeSerializer
    pagination_class = RecipePagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (
            User.objects.filter(
                subscribers__subscriber=self.request.user
            )
            .annotate(is_subscribed=Value(True, BooleanField()))
            .annotate(recipes_count=Count('recipes'))
        )
