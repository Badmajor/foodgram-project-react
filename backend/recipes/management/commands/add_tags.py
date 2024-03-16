import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Add tags'

    def handle(self, *args, **options):
        tags = []
        for tag_data in settings.TAGS_FOR_RECIPES:
            tag = Tag(**tag_data)
            tags.append(tag)
        try:
            Tag.objects.bulk_create(tags)
        except IntegrityError:
            logging.info('Tags are already exists')
