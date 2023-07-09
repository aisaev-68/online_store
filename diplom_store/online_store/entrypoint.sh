#!/bin/bash
apt install -y gettext
#python manage.py makemigrations
#python manage.py migrate
#python manage.py create_superuser
#python manage.py create_categories
#python manage.py create_tags
#python manage.py create_shop
#python manage.py create_products
python manage.py runserver 0.0.0.0:8000