# Generated by Django 4.2.1 on 2023-06-11 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_is_subscribed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_subscribed",
            field=models.BooleanField(default=False, verbose_name="Подписка оформлена"),
        ),
    ]
