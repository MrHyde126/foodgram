import csv
import logging.config
import os

from api.models import Ingredient
from django.core.management import BaseCommand
from foodgram.settings import BASE_DIR, LOGGING

logging.config.dictConfig(LOGGING)


class Command(BaseCommand):
    help = 'Загружает ингредиенты из CSV файла в папке data'

    def handle(self, *args, **options):
        file_path = os.path.join(BASE_DIR, 'data/ingredients.csv')

        with open(file_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    Ingredient(name=row[0], measurement_unit=row[1]).save()
                except Exception as exc:
                    logging.error(exc)

        return logging.info('Файл загружен.')
