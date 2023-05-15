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
        with open(str(Path(__file__).parent.joinpath('json_data-planshet.json'))) as json_file:
            data = json.load(json_file)
        prod_len = len(data)
        # user = User.objects.filter(username='editor').first()


        for value in data:
            error = {}
            try:
                request = requests.get(f"https://img.mvideo.ru/{value.get('image')}")
                request.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                error = {"Error": errh}
            except requests.exceptions.ConnectionError as errc:
                error = {"Error": errc}
            except requests.exceptions.Timeout as errt:
                error = {"Error": errt}
            except requests.exceptions.RequestException as err:
                error = {"Error": err}


            if not error.get("Error"):

                filename = str(uuid.uuid4())
                file_name = "{name}.{ext}".format(name=filename, ext='jpg')
                file_path = "product_images/{new_dir}/{image_name}".format(new_dir=new_dir_file,
                                                                           image_name=file_name)
                path_absolute = str(Path(uploaded_file_path, file_name))
                with open(path_absolute, 'wb') as f:
                    f.write(request.content)


                price = decimal.Decimal(value.get('item_base_price'))
                # rating = value.get('rating')
                # rating = decimal.Decimal()
                attributes = {}
                description = ''
                for values in value.get('propertiesPortion'):
                    for key, item in values.items():
                        if key == 'nameDescription':
                            description += str(item).replace('None', '')
                        if key == 'name':
                            attributes[item] = values['value']

                category = Category.objects.get(pk=12)
                product = Product.objects.create(
                            category=category,
                            title=value.get('name'),
                            fullDescription=description,
                            attributes=attributes,
                            price=price,
                            quantity=50,
                            tag=value.get('nameTranslit'),
                            brand=value.get('brandName')
                        )
                ProductImage.objects.create(image=file_path, product_id=product.pk)

                self.stdout.write(self.style.SUCCESS(f"Product {product} created"))


        self.stdout.write(self.style.SUCCESS("Products created"))