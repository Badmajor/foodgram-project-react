import csv
import json
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Add ingredients'

    def handle(self, *args, **options):
        count = 0
        path = os.path.join(settings.BASE_DIR, 'data/ingredients.json')
        with open(path, 'r', encoding='utf-8') as file:
            file_extension = file.name.split('.')[-1]
            if file_extension == 'csv':
                file_reader = csv.reader(file)
                for row in file_reader:
                    try:
                        Ingredient.objects.create(
                            name=row[0], measurement_unit=row[1])
                        count += 1
                    except IntegrityError:
                        continue

            elif file_extension == 'json':
                file_reader = json.load(file)
                for row in file_reader:
                    try:
                        Ingredient.objects.create(**row)
                        count += 1
                    except IntegrityError:
                        continue
        logging.info(f'Added {count} ingredients')
