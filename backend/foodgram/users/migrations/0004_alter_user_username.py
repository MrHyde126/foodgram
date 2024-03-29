# Generated by Django 4.2.1 on 2023-06-14 07:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_is_subscribed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=150,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[\\w.@+-]+\\z",
                        code="invalid_username",
                        message="Логин содержит недопустимые символы",
                    )
                ],
                verbose_name="Логин",
            ),
        ),
    ]
