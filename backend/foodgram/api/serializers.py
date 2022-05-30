from email.policy import default
from django.contrib.auth import get_user_model
from rest_framework import serializers
from recipes.models import Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag

from .fields import DecodingImageField, ImageRelatedField

User = get_user_model()


class CurrentRecipeDefault:
    requires_context = True

    def __call__(self, serializer_field):
        print('Context: ', serializer_field.context)
        return (
            serializer_field.context.get('request')
            .parser_context.get('kwargs').get('recipe_id')
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    measurement_unit = serializers.SlugRelatedField(
        'notation', read_only=True
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('name',)


class RecipeIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount')
    
    # При отображении запрашивать вложенный сериализатор
    # и дополнять ответ его данными без вложенности
    def to_representation(self, instance):
        representation = IngredientSerializer(instance.ingredient).data
        representation.update({'amount': instance.amount})
        return representation
    
    # Приведение данных к форме модели
    def to_internal_value(self, data):
        data['ingredient'] =  data.pop('id')
        return super().to_internal_value(data)


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):

    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = DecodingImageField()
    ingredients = RecipeIngredientSerializer(
        many=True,
        source = 'recipe_to_ingredients'
    )
    is_in_shopping_cart = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'is_in_shopping_cart',
            'ingredients', 'name', 'image', 'text', 'cooking_time'
        )
    
    # При отображении запрашивать вложенный сериализатор тегов
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags, many=True).data
        return representation
    
    def create(self, validated_data):
        # print('Validated_data: ', validated_data)
        recipe_items = validated_data.pop('recipe_to_ingredients')
        recipe = super().create(validated_data)
        for item in recipe_items:
            recipe.recipe_to_ingredients.create(**item)
        return recipe
    
    def update(self, instance, validated_data):
        # print('Validated_data (update): ', validated_data)
        recipe_items = validated_data.pop('recipe_to_ingredients')
        instance = super().update(instance, validated_data)
        instance.recipe_to_ingredients.all().delete()
        for item in recipe_items:
            instance.recipe_to_ingredients.create(**item)
        return instance


class ShoppingCartSerialzier(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    recipe = serializers.HiddenField(default=CurrentRecipeDefault())
    id = serializers.SlugRelatedField('id', source='recipe', read_only=True)
    name = serializers.SlugRelatedField('name', source='recipe', read_only=True)
    image = ImageRelatedField('image', source='recipe', read_only=True)
    cooking_time = serializers.SlugRelatedField('cooking_time', source='recipe', read_only=True)
    
    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'recipe', 'name', 'image', 'cooking_time')
        