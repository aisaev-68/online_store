from pathlib import Path, PurePath
from django.core.management import BaseCommand
import json

from tag.models import Tag


class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):

        self.stdout.write("Create tags")
        with open(str(Path(__file__).parent.joinpath('json_data-planshet.json'))) as json_file:
            data = json.load(json_file)

        tag_list = []
        for value in data:
            t = value.get('nameTranslit').split('-')[:2]
            for item in t:
                tag_list.append(item)
        tag_unique = list(set(tag_list))
        for item in tag_unique:
            tag = Tag.objects.create(id=item, name=item)
            self.stdout.write(self.style.SUCCESS(f"Tag {tag.name} added"))


        self.stdout.write(self.style.SUCCESS("Tags created"))