# Generated by Django 4.2.1 on 2023-06-11 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_subscribed",
            field=models.BooleanField(default=False),
        ),
    ]
