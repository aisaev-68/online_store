import decimal
import os
import random
import uuid
from pathlib import Path, PurePath
from mimesis import Text, Person, Numeric
from mimesis.locales import Locale
import itertools
from django.contrib.auth.models import User
from django.core.management import BaseCommand
import requests
import json

from django.utils.timezone import now

from catalog.models import Category
from product.models import ProductImage, Product, Manufacturer, Review, Seller, Specification
from tag.models import Tag

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
        person = Person(locale=Locale.RU)
        text = Text(locale=Locale.RU)
        number = Numeric()


        with open(str(Path(__file__).parent.joinpath('json_data-planshet.json'))) as json_file:
            data = json.load(json_file)
        prod_len = len(data)
        sellers = [shop for shop in Seller.objects.all()]
        category = Category.objects.get(title='Планшеты')

        with open(str(Path(__file__).parent.joinpath('specifications.json'))) as j_file:
            spec_data = json.load(j_file)

        Specification.objects.create(category_id=category.id, attributes=spec_data['Планшеты'])

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

                price = value.get('item_base_price')

                attributes = {}
                description = ''
                for values in value.get('propertiesPortion'):
                    for key, item in values.items():
                        if key == 'nameDescription':
                            description += str(item).replace('None', '')
                        if values[key] == "Размер экрана":
                            clean_string = values['value'].replace(' "value": "', '').replace('\"', '')
                            st = clean_string.split('/')
                            attributes["Размер экрана"] = st[0]
                            attributes["Разрешение экрана"] = st[1]
                        elif values[key] == "Встроенная память (ROM)":
                            attributes["Объем встроенной памяти"] = values['value'] + ' ' + 'ГБ'

                        elif values[key] == "Оперативная память":
                            attributes["Объем оперативной памяти"] = values['value'] + ' ' + 'ГБ'


                manufacturer, create = Manufacturer.objects.get_or_create(name=value.get('brandName'))
                product = Product.objects.create(
                    category=category,
                    title=value.get('name'),
                    fullDescription=description,
                    attributes=attributes,
                    price=price,
                    count=50,
                    brand=manufacturer,
                    seller=random.choice(sellers),
                    banner=random.choice([True, False])
                )
                ProductImage.objects.create(image=file_path, product_id=product.pk)

                t = value.get('nameTranslit').split('-')[:2]
                tag_list = []
                for item in t:
                    tag_list.append(Tag.objects.filter(name=item).first())

                product.tags.add(tag_list[0], tag_list[1])

                Review.objects.create(author=person.full_name(), email=person.email(), text=text.text(), rate=number.integer_number(start=0, end=5), product=product)

                self.stdout.write(self.style.SUCCESS(f"Product {product} created"))

        self.stdout.write(self.style.SUCCESS("Products created"))
