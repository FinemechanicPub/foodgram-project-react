from django.contrib import admin
from django.forms import TextInput

from .models import Recipe, Ingredient, Unit, Tag


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time')
    exclude = ('ingredients',)
    inlines = (IngredientInline,)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    prepopulated_fields = {'slug': ('name',)}
    widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
