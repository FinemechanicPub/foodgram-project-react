from django.contrib import admin

from .models import Favorite, Recipe, Ingredient, ShoppingCart, Tag, Unit


class IngredientInline(admin.TabularInline):
    """Вложенная форма ингредиентов рецепта"""
    model = Recipe.ingredients.through
    fields = ('ingredient', 'amount',)
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['ingredient'].queryset = (
            formset.form.base_fields['ingredient']
            .queryset.select_related('measurement_unit')
        )
        return formset


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time')
    exclude = ('ingredients',)
    inlines = (IngredientInline,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    list_editable = ('color',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'notation',)
    search_fields = ('notation',)
