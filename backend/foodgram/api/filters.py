import django_filters
from rest_framework.filters import SearchFilter

from .models import Ingredient, Recipe, Tag


class IngredientFilter(SearchFilter):
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.BooleanFilter(
        widget=django_filters.widgets.BooleanWidget()
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        widget=django_filters.widgets.BooleanWidget()
    )
    author = django_filters.CharFilter(field_name='author')
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')
