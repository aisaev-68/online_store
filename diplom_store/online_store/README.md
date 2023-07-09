### 1 этап
1. Создание нового Django-проекта
2. Разработка модели хранения данных
3. Разработка структуры URL на сайте.

| Раздел | Страница     | Описание                 | HTTP-метод | URL       | Пространство имен |
|--------|--------------|--------------------------|------------|-----------|-------------------|
|Главная страница| registr.html | Регистарция пользователя | POST       | register/ | register          |
|Главная страница| login.html   | Вход                     | GET        | login/    | login             |
|Главная страница| cart.html    | Корзина                  | GET        | cart/     | cart              |
|Личный кабинет|              | Выход                    | GET        | logout/   | logout            |
|Личный кабинет| registr.html | Регистарция пользователя | POST       | register/ | register          |
4. Разработка каркаса приложения
5. Интеграция вёрстки шаблона сайта
6. Подключение административной панели и БД
7. Разработка верхнего меню и футера


### Переменные среды
Переименовать файл .env.example в .env и установите свои данные

### Команды для сборки и запуска

1. Установить зависимости окружения: 
```
poetry install
```
2. Активация окружения: 
```
poetry shell
```
3. Миграция данных: 
```
python manage.py makemigrations
python manage.py migrate
```
4. Заполнение базы тестовыми данными:
```
cd djmarketplace
python manage.py create_superuser
python manage.py create_room_type
python manage.py create_houses
python manage.py create_news
```
5. Текстуры
```
python manage.py dumpdata online_store.Catalog > online_store/tests/fixtures/catalog-fixtures.json
python manage.py dumpdata online_store.Catalog > online_store/tests/fixtures/catalog-fixtures.json
python manage.py dumpdata houseroom.RoomType > houseroom/tests/fixtures/room_type-fixtures.json  
python manage.py dumpdata houseroom.NumberRoom > houseroom/tests/fixtures/number_room-fixtures.json 
python manage.py dumpdata news.News > houseroom/tests/fixtures/news-fixtures.json    
```
5. Запуск приложения в режиме разработки:
```
python manage.py runserver
```

6. Сайт
```
http://127.0.0.1:8080
```

sudo apt install gettext

python manage.py makemessages -l en -l ru
python manage.py compilemessages

django-admin makemessages --all --ignore=.venv
django-admin compilemessages --ignore=.venv

docker-compose logs online_store_megano_1

https://ejudge.lksh.ru/lang_docs/djbook.ru/rel1.9/topics/db/queries.html