import csv
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Add data into db from JSON of CSV files'

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'data/ingredients.json')
        with open(path, 'r', encoding='utf-8') as file:
            file_extension = file.name.split('.')[-1]
            ingredients = []
            if file_extension == 'csv':
                file_reader = csv.reader(file)
                for row in file_reader:
                    ingredient = Ingredient(
                        name=row[0], measurement_unit=row[1])
                    ingredients.append(ingredient)
            elif file_extension == 'json':
                file_reader = json.load(file)
                for row in file_reader:
                    ingredient = Ingredient(**row)
                    ingredients.append(ingredient)
            Ingredient.objects.bulk_create(ingredients)
