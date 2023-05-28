import json
import os
import shutil
from django.core.management import BaseCommand

from catalog.models import Category


class Command(BaseCommand):
    """
    Команда для первоначальной загрузки каталогов и категорий.
    Выполняется из терминала: python manage.py create_categories
    """

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                f"Start added catalog and category"
            )
        )
        BASE_DIR_MEDIA = os.path.abspath('media/')  # путь папки media
        if not os.path.exists(os.path.join(BASE_DIR_MEDIA, 'catalog')):
            os.mkdir(os.path.join(BASE_DIR_MEDIA, 'catalog'))

        if not os.path.exists(os.path.join(BASE_DIR_MEDIA, 'category')):
            os.mkdir(os.path.join(BASE_DIR_MEDIA, 'category'))

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # папка запуска модуля

        with open(os.path.join(BASE_DIR, 'commands/catalog-data.json')) as json_file:
            catalogs = json.load(json_file)

        for catalog in catalogs:
            item_catalog = Category.objects.create(
                title=catalog["fields"]["title"],
                src=catalog["fields"]["src"],
            )

            src_path = os.path.join(BASE_DIR, f"commands/{catalog['fields']['src']}")
            dst_path = os.path.join(BASE_DIR_MEDIA, f"{catalog['fields']['src']}")
            shutil.copyfile(src_path, dst_path)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Added item catalog {item_catalog}"
                )
            )

        with open(os.path.join(BASE_DIR, 'commands/category-data.json')) as json_file:
            categories = json.load(json_file)

        id_catalog = Category.objects.filter(title='Электроника').first()
        for category in categories:
            if category['fields']['catalog'] == 1:
                item_category = Category.objects.create(
                    title=category['fields']['title'],
                    src=category['fields']['src'],
                    parent=id_catalog)

                src_path = os.path.join(BASE_DIR, f"commands/{category['fields']['src']}")
                dst_path = os.path.join(BASE_DIR_MEDIA, f"{category['fields']['src']}")
                shutil.copyfile(src_path, dst_path)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Added item category {item_category}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added category"
            )
        )
