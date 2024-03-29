# Generated by Django 4.2.1 on 2023-06-22 07:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0011_alter_recipe_cooking_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="cooking_time",
            field=models.PositiveIntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(
                        limit_value=1,
                        message="Время приготовления не может быть меньше 1 мин.",
                    )
                ],
                verbose_name="Время приготовления (в минутах)",
            ),
        ),
    ]
