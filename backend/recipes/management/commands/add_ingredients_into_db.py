import csv
import json
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Add data into db from JSO files'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to .json or .csv file')

    def handle(self, *args, **options):
        path = os.path.normpath(options['file_path'])
        with open(path, 'r', encoding='utf-8') as file:
            file_extension = file.name.split('.')[-1]
            ingredients = []
            if file_extension == 'csv':
                file_reader = csv.reader(file)
                for row in file_reader:
                    ingredient = Ingredient(name=row[0], measurement_unit=row[1])
                    ingredients.append(ingredient)
            elif file_extension == 'json':
                file_reader = json.load(file)
                for row in file_reader:
                    ingredient = Ingredient(**row)
                    ingredients.append(ingredient)
            Ingredient.objects.bulk_create(ingredients)





