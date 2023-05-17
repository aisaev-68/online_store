import decimal
import os
import random
import uuid
from pathlib import Path, PurePath
import itertools
from django.contrib.auth.models import User

from django.core.management import BaseCommand
import requests
import json

from django.utils.timezone import now

from catalog.models import Category
from product.models import ProductImage, Product
from tag.models import Tag


class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):

        self.stdout.write("Create tags")
        with open(str(Path(__file__).parent.joinpath('json_data-tags.json'))) as json_file:
            data = json.load(json_file)
        category_id = Category.objects.filter(title='Планшеты').first().id

        product = Product.objects.filter(category_id=category_id).first()

        for tag in data:
            tag = Tag.objects.create(name=tag['name'])
            tag.category = category_id
            tag.save()
            self.stdout.write(self.style.SUCCESS(f"Tag {tag.name} added"))


        self.stdout.write(self.style.SUCCESS("Tags created"))