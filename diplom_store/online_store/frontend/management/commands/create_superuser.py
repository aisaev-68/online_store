from django.core.management.base import BaseCommand, CommandError

from account.models import User
from online_store import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        # The magic line

        User.objects.create_superuser(
            username=settings.USER_ADMIN,
            email=settings.EMAIL,
            password=settings.PASSWORD,
            phone="89285484431",
            last_name="Иванов",
            first_name="Иван",
            surname="Иванович",
        )