from django.core.validators import MinValueValidator
from django.db import models
from foodgram.settings import MIN_AMOUNT
from users.models import User


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name[:30]}, {self.measurement_unit[:30]}'


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет в HEX', max_length=7, unique=True)
    slug = models.SlugField('Уникальный слаг', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение', upload_to='media/')
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredientAmount',
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                limit_value=MIN_AMOUNT,
                message=(
                    f'Время приготовления не может быть меньше {MIN_AMOUNT}'
                ),
            )
        ],
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.name[:30]} ({self.author.username[:30]})'


class RecipeIngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='recipe_ing',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='recipe_ing',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                limit_value=MIN_AMOUNT,
                message=f'Количество не может быть меньше {MIN_AMOUNT}',
            )
        ],
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        ordering = ('recipe__name',)

    def __str__(self):
        return f'{self.recipe.name[:30]} содержит {self.ingredient.name[:30]}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='fav_recipes',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='fav_recipes',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_fav_recipe'
            )
        ]

    def __str__(self):
        return (
            f'{self.user.username[:30]} добавил в избранное'
            f' {self.recipe.name[:30]}'
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shopping'
            )
        ]

    def __str__(self):
        return (
            f'{self.user.username[:30]} добавил в список покупок'
            f' {self.recipe.name[:30]}'
        )
