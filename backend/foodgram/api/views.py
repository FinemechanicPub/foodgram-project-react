from django.db.models import OuterRef, Exists, Value, BooleanField, Prefetch
from django.contrib.auth import get_user_model
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from djoser.views import UserViewSet
from requests import Response
from rest_framework import viewsets, decorators, exceptions, response, status
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from recipes.services import ShoppingList
from users.models import Subscription

from .filters import IngredientFilter, RecipeFilter
from .pagination import RecipePagination
from .serializers import FavoritesSerializer, IngredientSerializer, RecipeSerializer, RecipeShortSerializer, ShoppingCartSerialzier, SubscriptionSerializer, TagSerializer, UserRecipeSerializer


User = get_user_model()


def is_subscribed_annotation(queryset, user):
    if user.is_authenticated:            
        return queryset.annotate(
            is_subscribed=Exists(
                Subscription.objects.filter(
                    subscriber=user,
                    author=OuterRef('pk')
                )
            )
        )
    else:
        return queryset.annotate(is_subscribed=Value(False, BooleanField()))



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

    def get_queryset(self):

        queryset = self.queryset.prefetch_related(Prefetch(
            'author',
            is_subscribed_annotation(User.objects.all(), self.request.user)
        ))
        if self.request.user.is_authenticated:
            return queryset.annotate(
                is_in_shopping_cart=Exists(
                    ShoppingCart.objects.filter(
                        recipe=OuterRef('pk'),
                        user=self.request.user
                    )
                ),
                is_favorited=Exists(
                    Favorite.objects.filter(
                        recipe=OuterRef('pk'),
                        user=self.request.user
                    )
                )
            )
        return queryset.annotate(
            is_in_shopping_cart=Value(0, BooleanField()),
            is_favorited=Value(0, BooleanField())
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
    
    @decorators.action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        shopping_list = ShoppingList(request.user)
        return FileResponse(shopping_list.as_txt('my_shopping_list'), as_attachment=True)
        

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

    @decorators.action(detail=True, methods=['POST', 'DELETE'])
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

    def get_queryset(self):
        return User.objects.filter(
            subscribers__subscriber=self.request.user
        )