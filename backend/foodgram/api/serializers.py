from email.policy import default
from django.contrib.auth import get_user_model
from rest_framework import serializers
from recipes.models import Favorite, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag
from users.models import Subscription

from .fields import DecodingImageField

User = get_user_model()


class URLParameter():
    """Значение по умолчанию из параметров URL"""
    requires_context = True

    def __init__(self, field_name):
        self.field_name = field_name

    def __call__(self, serializer_field):        
        return (
            serializer_field.context.get('request')
            .parser_context.get('kwargs').get(self.field_name)
        )


class CurrentRecipeDefault:
    """Значение по умолчания для рецепта, извлекаемое из URL"""
    requires_context = True

    def __call__(self, serializer_field):
        print('Context: ', serializer_field.context)
        return (
            serializer_field.context.get('request')
            .parser_context.get('kwargs').get('recipe_id')
        )
     

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )
        


class TagSerializer(serializers.ModelSerializer):
    """"Сериализатор тегов"""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента"""
    measurement_unit = serializers.SlugRelatedField(
        'notation', read_only=True
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('name',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор списка ингредиентов рецепта"""
    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount')
    
    # При отображении запрашивать вложенный сериализатор
    # и дополнять ответ его данными без вложенности
    def to_representation(self, instance):
        """Генератор представления с уплощением структуры ответа"""
        representation = IngredientSerializer(instance.ingredient).data
        representation.update({'amount': instance.amount})
        return representation
    
    # Приведение данных к форме модели
    def to_internal_value(self, data):
        """Генератор внутреннего представления с заменой имени поля"""
        data['ingredient'] =  data.pop('id')
        return super().to_internal_value(data)


class RecipeShortSerializer(serializers.ModelSerializer):
    """Краткая форма сериализатора рецептов"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    """Развернутая форма сериализатора рецептов"""
    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = DecodingImageField()
    ingredients = RecipeIngredientSerializer(
        many=True,
        source = 'recipe_to_ingredients'
    )
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'is_in_shopping_cart', 'is_favorited',
            'ingredients', 'name', 'image', 'text', 'cooking_time'
        )
    
    # При отображении запрашивать вложенный сериализатор тегов
    def to_representation(self, instance):
        """Генератор представления с развернутым отображением тегов"""
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags, many=True).data
        return representation
    
    def create(self, validated_data):
        """Создание записи с обработкой вложенных данных по ингредиентам"""
        # print('Validated_data: ', validated_data)
        recipe_items = validated_data.pop('recipe_to_ingredients')
        recipe = super().create(validated_data)
        for item in recipe_items:
            recipe.recipe_to_ingredients.create(**item)
        return recipe
    
    def update(self, instance, validated_data):
        """Обновление записи с обработкой вложенных данных по ингредиентам"""
        # print('Validated_data (update): ', validated_data)
        recipe_items = validated_data.pop('recipe_to_ingredients')
        instance = super().update(instance, validated_data)
        instance.recipe_to_ingredients.all().delete()
        for item in recipe_items:
            instance.recipe_to_ingredients.create(**item)
        return instance


class RecipeListSerializer(serializers.ModelSerializer):
    """Базовый сериализатор добавления рецепта к списку рецептов"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    recipe = serializers.HiddenField(default=CurrentRecipeDefault())    
    
    class Meta:
        fields = ('user', 'recipe')


class ShoppingCartSerialzier(RecipeListSerializer):
    """Сериализатор добавления рецепта к списку покупок"""
    class Meta(RecipeListSerializer.Meta):
        model = ShoppingCart


class FavoritesSerializer(RecipeListSerializer):
    """"Сериализатор добавления рецепта к списку избранного"""
    class Meta(RecipeListSerializer.Meta):
        model = Favorite
        

class UserRecipeSerializer(UserSerializer):
    """Сериализатор пользователя и его рецептов"""
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.IntegerField(read_only=True)

    def get_recipes(self, obj):
        recipes_limit = int(
            self.context.get('request').query_params.get('recipes_limit', 0)
        )
        return RecipeShortSerializer(
            obj.recipes.all()[:recipes_limit], many=True
        ).data

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')        


class SubscriptionSerializer(serializers.ModelSerializer):

    subscriber = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = serializers.HiddenField(default=URLParameter('user_id'))   

    class Meta:
        model = Subscription
        fields = ('subscriber', 'author')