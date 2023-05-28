import json
from pathlib import Path

from django.utils.timezone import now
from mimesis import Address, Finance
from mimesis.locales import Locale
from django.core.management import BaseCommand


from product.models import Seller, Manufacturer



class Command(BaseCommand):
    """
    Creates shop
    """

    def handle(self, *args, **options):
        self.stdout.write("Create sellers and manufacturers")

        self.stdout.write("Create manufacturers")
        with open(str(Path(__file__).parent.joinpath('manufacturer-json.json'))) as json_file:
            data = json.load(json_file)
        for value in data:
            manufacturer = Manufacturer.objects.create(name=value['name'])
            self.stdout.write(f"Create {manufacturer}")

        self.stdout.write("Created manufacturers")

        self.stdout.write("Create sellers")
        for _ in range(20):
            name = Finance(locale=Locale.RU)
            address = Address(locale=Locale.RU)

            seller = Seller.objects.create(
                name=name.company(),
                city=address.city(),
                address=address.address(),
            )
            self.stdout.write(f"Created {seller}")
        self.stdout.write("Created sellers")

        self.stdout.write(self.style.SUCCESS("Sellers created"))
