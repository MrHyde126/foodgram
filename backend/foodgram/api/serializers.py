import base64

from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from foodgram.settings import MIN_VALUE
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from users.models import Subscription, User

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredientAmount,
    ShoppingCart,
    Tag,
)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and Subscription.objects.filter(user=user, author=author).exists()
        )


class UserSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author'),
                message='Такая подписка уже оформлена!',
            ),
        ]

    def validate(self, data):
        if self.context.get('request').user == data['author']:
            raise serializers.ValidationError(
                'Невозможно подписаться на себя!'
            )
        return data

    def to_representation(self, instance):
        return UserSerializer(
            instance.author, context={'request': self.context.get('request')}
        ).data


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, author):
        recipes = recipes_limit = None
        request = self.context.get('request')
        if request:
            recipes_limit = request.query_params.get('recipes_limit')
        recipes = (
            author.recipes.all()[: int(recipes_limit)]
            if recipes_limit
            else author.recipes.all()
        )
        return RecipePartialSerializer(
            recipes, many=True, context={'request': request}
        ).data

    def get_recipes_count(self, author):
        return author.recipes.count()

    def get_is_subscribed(self, author):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Subscription.objects.filter(
                user=request.user, author=author
            ).exists()
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAddSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredientAmount
        fields = ('id', 'amount')


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = RecipeIngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    color = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                message='Укажите цвет в HEX формате!',
                code='invalid_color',
            )
        ],
        required=True,
        max_length=7,
    )

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ingredients = IngredientAddSerializer(many=True, source='ingredient')
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('author', 'recipe'),
                message='У пользователя уже есть такой рецепт!',
            ),
        ]

    def validate(self, data):
        list_of_ingredients = []
        for ingredient in data.get('ingredient'):
            if ingredient.get('amount') < MIN_VALUE:
                raise serializers.ValidationError(
                    {
                        'id': [
                            'Количество ингредиента не должно быть меньше'
                            f' {MIN_VALUE}!'
                        ]
                    }
                )
            list_of_ingredients.append(ingredient.get('id'))
        if len(set(list_of_ingredients)) != len(list_of_ingredients):
            raise serializers.ValidationError(
                {
                    'id': [
                        'В рецепте не должно быть повторяющихся ингредиентов!'
                    ]
                }
            )
        return data

    @staticmethod
    def add_ingredients(recipe, ingredients):
        list_of_ingredients = []
        for ingredient in ingredients:
            cur_ingredient = get_object_or_404(
                Ingredient, id=ingredient.get('id')
            )
            list_of_ingredients.append(
                RecipeIngredientAmount(
                    recipe=recipe,
                    ingredient=cur_ingredient,
                    amount=ingredient.get('amount'),
                )
            )
        RecipeIngredientAmount.objects.bulk_create(list_of_ingredients)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredient')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredient')
        instance.ingredients.clear()
        self.add_ingredients(instance, ingredients)
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeRetrieveSerializer(
            instance, context={'request': self.context.get('request')}
        ).data


class RecipeRetrieveSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    image = Base64ImageField(read_only=True)
    ingredients = IngredientsInRecipeSerializer(
        many=True, source='recipe_ing', read_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and Favorite.objects.filter(user=user, recipe=recipe).exists()
        )

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and ShoppingCart.objects.filter(user=user, recipe=recipe).exists()
        )


class RecipePartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже в списке избранного!',
            ),
        ]

    def to_representation(self, instance):
        return RecipePartialSerializer(
            instance.recipe, context={'request': self.context.get('request')}
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже в списке покупок!',
            ),
        ]

    def to_representation(self, instance):
        return RecipePartialSerializer(
            instance.recipe, context={'request': self.context.get('request')}
        ).data
