import decimal
import os
import random
import uuid
from pathlib import Path, PurePath
import itertools
from django.contrib.auth.models import User
from django.core.checks import Tags
from django.core.management import BaseCommand
import requests
import json

from django.utils.timezone import now

from catalog.models import Category
from product.models import ProductImage, Product



class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):

        self.stdout.write("Create tags")
        with open(str(Path(__file__).parent.joinpath('json_data-tags.json'))) as json_file:
            data = json.load(json_file)

        for tag in data:
            Tags.objects.create(name=tag['name'])
            self.stdout.write(self.style.SUCCESS(f"Product {product} created"))


        self.stdout.write(self.style.SUCCESS("Products created"))