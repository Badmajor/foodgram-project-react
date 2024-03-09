from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Add tags'

    def handle(self, *args, **options):
        tags = []
        for tag_data in settings.TAGS_FOR_RECIPES:
            tag = Tag(**tag_data)
            tags.append(tag)
        Tag.objects.bulk_create(tags)