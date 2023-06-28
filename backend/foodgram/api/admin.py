from django.contrib import admin
from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet

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
    list_filter = ('name',)
    list_per_page = 30


class RequiredInlineFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        if not self.cleaned_data:
            raise ValidationError(
                'Должно присутствовать хотя бы одно значение!'
            )


class IngredientInline(admin.StackedInline):
    model = RecipeIngredientAmount
    autocomplete_fields = ('ingredient',)
    min_num = 1
    extra = 1
    formset = RequiredInlineFormSet


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
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
