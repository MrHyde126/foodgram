# Generated by Django 4.2.1 on 2023-06-17 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_alter_favorite_recipe"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favorite",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fav_recipes",
                to="api.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AlterField(
            model_name="recipeingredientamount",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient",
                to="api.ingredient",
                verbose_name="Ингредиент",
            ),
        ),
        migrations.AlterField(
            model_name="recipeingredientamount",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipe",
                to="api.recipe",
                verbose_name="Рецепт",
            ),
        ),
    ]
