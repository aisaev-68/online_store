from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, last_name, first_name, surname, phone, password=None, avatar=None):

        if not username:
            raise ValueError(_('Users must have a username'))

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            last_name=last_name,
            first_name=first_name,
            surname=surname,
            phone=phone,
            avatar=avatar,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, last_name, first_name, surname, phone, password=None, avatar=None):
        user = self.create_user(
            email=email,
            username=username,
            last_name=last_name,
            first_name=first_name,
            surname=surname,
            phone=phone,
            avatar=avatar,
        )

        user.save(using=self._db)
        return user