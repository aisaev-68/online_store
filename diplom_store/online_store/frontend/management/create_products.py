import os
import random
import uuid
from pathlib import Path, PurePath

from django.contrib.auth.models import User
from django.core.management import BaseCommand
import requests
import json

from django.utils.timezone import now

from shopapp.models import Product, Category, Catalog

new_dir_file = now().date().strftime("%Y/%m/%d")
uploaded_file_path = Path().parent / "media/product_images" / new_dir_file
uploaded_file_path.mkdir(exist_ok=True, parents=True)
uploaded_file_path = uploaded_file_path.absolute()


class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):

        self.stdout.write("Create products")
        with open(str(Path(__file__).parent.joinpath('json_data-products.json'))) as json_file:
            data = json.load(json_file)

        user = User.objects.filter(username='editor').first()
        category = Category.objects.filter(name='Телефоны и смарт часы').first()

        for d in data["data"]:

            request = requests.get(d['image'])
            filename = str(uuid.uuid4())
            file_name = "{name}.{ext}".format(name=filename, ext='jpg')
            file_path = "product_images/{new_dir}/{image_name}".format(new_dir=new_dir_file, image_name=file_name)
            path_absolute = str(Path(uploaded_file_path, file_name))
            with open(path_absolute, 'wb') as f:
                f.write(request.content)

            Product.objects.create(
                category=category,
                title=d['name'],
                fullDescription=d['description'],
                rating=d.get('rating'),
                price=d['price'],
                discount=random.choices([5, 10, 15, 20])[0],
                count=50,
                archived=False,
            )

        self.stdout.write(self.style.SUCCESS("Products created"))
