from django.core.management.base import BaseCommand, CommandError

from account.models import User
from online_store import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        # The magic line
        self.stdout.write("Create admin")

        User.objects.create_superuser(
            username=settings.USER_ADMIN,
            email=settings.EMAIL,
            password=settings.PASSWORD,
            phone="89285484431",
            last_name="Иванов",
            first_name="Иван",
            surname="Иванович",
        )
        self.stdout.write("Create anonymous user")
        anonymous, created = User.objects.get_or_create(username=settings.ANONYMOUS_USER)

        # Задаем пароль для анонимного пользователя
        anonymous.set_password(settings.ANONYMOUS_USER_PASSWORD)
        anonymous.save()