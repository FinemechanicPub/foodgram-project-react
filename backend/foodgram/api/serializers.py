from django.contrib.auth import get_user_model
from rest_framework import serializers
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    measurement_unit = serializers.SlugRelatedField(
        'notation', read_only=True
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    
    ingredient = IngredientSerializer()    

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount')
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ingredient = representation.pop('ingredient')
        ingredient.update(representation)
        return ingredient


class RecipeSerializer(serializers.ModelSerializer):

    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        read_only=True,
        source='recipe_to_ingredients'
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )

        