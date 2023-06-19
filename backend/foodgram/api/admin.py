from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredientAmount,
    ShoppingCart,
    Tag,
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    list_per_page = 30


class RecipeIngredientAdmin(admin.StackedInline):
    model = RecipeIngredientAmount
    autocomplete_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientAdmin,)
    list_display = ('name', 'author', 'fav_recipe_count')
    search_fields = ('name', 'tags')
    list_filter = ('author', 'name', 'tags')
    list_per_page = 30

    @admin.display(description='Число добавлений рецепта в избранное')
    def fav_recipe_count(self, recipe):
        return recipe.fav_recipes.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name', 'slug')
    list_filter = ('color',)
    list_per_page = 30


@admin.register(RecipeIngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe',)
    list_per_page = 30


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    search_fields = ('user', 'recipe')
    list_filter = ('user',)
    list_per_page = 30


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    search_fields = ('user', 'recipe')
    list_filter = ('user',)
    list_per_page = 30
