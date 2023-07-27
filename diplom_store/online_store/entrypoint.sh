#!/bin/bash
apt install -y gettext
python manage.py makemigrations
python manage.py migrate
python manage.py create_groups
python manage.py create_categories
python manage.py create_tags
python manage.py create_shop
python manage.py create_products
python manage.py dumpdata account > tests/fixtures/user_and_group-fixtures.json
python manage.py dumpdata catalog > tests/fixtures/catalog-fixtures.json
python manage.py dumpdata order > tests/fixtures/order-fixtures.json
python manage.py dumpdata payment > tests/fixtures/payment-fixtures.json
python manage.py dumpdata product > tests/fixtures/product-fixtures.json
python manage.py dumpdata settings > tests/fixtures/settings-fixtures.json
python manage.py dumpdata tag > tests/fixtures/tag-fixtures.json
python manage.py runserver 0.0.0.0:8000