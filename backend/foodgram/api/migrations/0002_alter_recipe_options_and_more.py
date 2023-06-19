# Generated by Django 4.2.1 on 2023-06-15 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipe",
            options={
                "ordering": ("-id",),
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
            },
        ),
        migrations.AlterModelOptions(
            name="recipeingredientamount",
            options={
                "ordering": ("ingredient",),
                "verbose_name": "Ингредиент в рецепте",
                "verbose_name_plural": "Ингредиенты в рецепте",
            },
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="is_favorited",
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="is_in_shopping_cart",
        ),
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(upload_to="media/", verbose_name="Изображение"),
        ),
        migrations.AlterField(
            model_name="recipeingredientamount",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient_amount",
                to="api.ingredient",
                verbose_name="Ингредиент",
            ),
        ),
        migrations.AlterField(
            model_name="recipeingredientamount",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient_amount",
                to="api.recipe",
                verbose_name="Рецепт",
            ),
        ),
    ]
