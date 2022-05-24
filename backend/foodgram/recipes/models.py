from tabnanny import verbose
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


def cut_text_display(text):
    """Обрезание текста при выводе на экран"""
    return text[:settings.RECIPES['TEXT_DISPLAY_LENGTH']]


class Unit(models.Model):
    """Единицы измерения"""
    notation = models.CharField('обозначение', max_length=200)

    class Meta:
        default_related_name = 'units'
        verbose_name = 'единица измерения'
        verbose_name_plural = 'единицы измерения'

    def __str__(self) -> str:
        return cut_text_display(self.notation)


class Ingredient(models.Model):
    """Ингрeдиент"""
    name = models.CharField('название', max_length=200)
    units = models.ForeignKey(Unit, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'ingredients'
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self) -> str:
        return cut_text_display(f'{self.name}, {self.units}')


class Tag(models.Model):
    "Тег"
    name = models.CharField('название', max_length=200)
    color = models.CharField(
        'цвет в шестнадцатиричном формате',
        max_length=7,
        null=True
    )
    slug = models.SlugField('код', unique=True, null=True)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self) -> str:
        return cut_text_display(self.name)






class Recipe(models.Model):
    "Рецепт"
    name = models.CharField('название', max_length=200)
    text = models.TextField('описание')
    image = models.ImageField('изображение')
    cooking_time = models.PositiveSmallIntegerField(
        'время приготовления (в минутах)',
        validators=(MinValueValidator(1, message='не меньше 1 минуты'),)
    )
    author = models.ForeignKey(
        User,
        verbose_name='автор',
        on_delete=models.SET_NULL,
        null=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='ингредиенты'
    )
    tags = models.ManyToManyField(Tag, verbose_name='теги')

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self) -> str:
        return cut_text_display(self.name)


class RecipeIngredient(models.Model):
    """Ингредиент в составе рецепта"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, verbose_name='ингредиент', on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        'количество',
        validators=(MinValueValidator(1, 'не меньше 1'),)
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'состав'