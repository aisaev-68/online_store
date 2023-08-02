from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from mimesis import Person
from mimesis.locales import Locale
from mimesis.enums import Gender
from django.utils.translation import gettext_lazy as _

from account.models import User
from order.models import Order, OrderProducts
from product.models import Product, Sale, Seller, Specification, Manufacturer, ProductImage, Review
from catalog.models import Category
from settings.models import PaymentSettings
from payment.models import Payment
from tag.models import Tag
from online_store import settings


class Command(BaseCommand):
    help = _('Creates read only default permission groups for users')

    def handle(self, *args, **options):
        self.stdout.write("Create groups")
        admin_group, created = Group.objects.get_or_create(name="Admin")
        clients_group, created = Group.objects.get_or_create(name="Clients")

        content_type_product = ContentType.objects.get_for_model(Product)
        product_permission = Permission.objects.filter(content_type=content_type_product)
        for perm in product_permission:
            admin_group.permissions.add(perm)

            if perm.codename == "view_product":
                clients_group.permissions.add(perm)

        content_type_product_image = ContentType.objects.get_for_model(ProductImage)
        product_image_permission = Permission.objects.filter(content_type=content_type_product_image)
        for perm in product_image_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_product_image":
                clients_group.permissions.add(perm)

        content_type_category = ContentType.objects.get_for_model(Category)
        category_permission = Permission.objects.filter(content_type=content_type_category)
        for perm in category_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_category":
                clients_group.permissions.add(perm)

        content_type_review = ContentType.objects.get_for_model(Review)
        review_permission = Permission.objects.filter(content_type=content_type_review)
        for perm in review_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_review":
                clients_group.permissions.add(perm)

        content_type_tag = ContentType.objects.get_for_model(Tag)
        tag_permission = Permission.objects.filter(content_type=content_type_tag)
        for perm in tag_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_tag":
                clients_group.permissions.add(perm)

        content_type_sale = ContentType.objects.get_for_model(Sale)
        sale_permission = Permission.objects.filter(content_type=content_type_sale)
        for perm in sale_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_sale":
                clients_group.permissions.add(perm)

        content_type_seller = ContentType.objects.get_for_model(Seller)
        seller_permission = Permission.objects.filter(content_type=content_type_seller)
        for perm in seller_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_seller":
                clients_group.permissions.add(perm)

        content_type_manufacturer = ContentType.objects.get_for_model(Manufacturer)
        manufacturer_permission = Permission.objects.filter(content_type=content_type_manufacturer)
        for perm in manufacturer_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_manufacturer":
                clients_group.permissions.add(perm)

        content_type_specification = ContentType.objects.get_for_model(Specification)
        specification_permission = Permission.objects.filter(content_type=content_type_specification)
        for perm in specification_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_specification":
                clients_group.permissions.add(perm)

        content_type_settings = ContentType.objects.get_for_model(PaymentSettings)
        settings_permission = Permission.objects.filter(content_type=content_type_settings)
        for perm in settings_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_settings":
                clients_group.permissions.add(perm)

        content_type_order = ContentType.objects.get_for_model(Order)
        order_permission = Permission.objects.filter(content_type=content_type_order)
        for perm in order_permission:
            admin_group.permissions.add(perm)
            clients_group.permissions.add(perm)

        content_type_order_product = ContentType.objects.get_for_model(OrderProducts)
        order_product_permission = Permission.objects.filter(content_type=content_type_order_product)
        for perm in order_product_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_order_product":
                clients_group.permissions.add(perm)

        content_type_payment = ContentType.objects.get_for_model(Payment)
        post_permission = Permission.objects.filter(content_type=content_type_payment)
        for perm in post_permission:
            admin_group.permissions.add(perm)
            clients_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS("Groups created"))
        self.stdout.write(self.style.SUCCESS("Create superuser"))
        User.objects.create_superuser(
            username='superuser',
            email='email@ya.ru',
            password='12345',
            phone="89285484431",
            last_name="Петров",
            first_name="Петр",
            surname="Петрович",
        )
        admin_user = User.objects.create_user(
            username=settings.USER_ADMIN,
            email=settings.EMAIL,
            password=settings.PASSWORD,
            phone="89305484111",
            last_name="Иванов",
            first_name="Иван",
            surname="Иванович",
            is_staff=True,
        )
        admin_group = Group.objects.get(name="Admin")
        admin_user.groups.add(admin_group)
        self.stdout.write(self.style.SUCCESS(f"{admin_user} added in Admin group"))

        for _ in range(20):
            person = Person(locale=Locale.RU)
            client_user = User.objects.create_user(
                username=person.username(),
                first_name=person.first_name(gender=Gender.MALE),
                last_name=person.last_name(gender=Gender.MALE),
                surname=person.surname(gender=Gender.MALE),
                email=person.email(),
                phone=person.telephone('7##########'),
                password='12345',
            )

            client_group = Group.objects.get(name="Clients")
            client_user.groups.add(client_group)

            self.stdout.write(self.style.SUCCESS(f"{client_user} added in Clients group"))

        self.stdout.write(self.style.SUCCESS("Process end successful."))
