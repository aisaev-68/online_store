### Интернет-магазин Мегано

### Переменные среды
Переименовать файл .env.example в .env и установите свои данные

### Команды для сборки и запуска

1. Собрать образы и запустить сервисы (при запуске сервисов происходить миграция и заполнение баз тестовыми данным): 
```
docker-compose up -d --build # режим prod
```
3. Просмотр статуса службы:
```
docker-compose ps -a
```

### Другие команды работы с docker

1. Перезапустить службу:
```
 docker-compose restart
```
2. Запустить службу:
```
docker-compose start <имя службы>
```
3. Остановить службу:
```
docker-compose stop <имя службы>
```
4. Закрыть службы и удалить контейнеры:
```
docker container stop $(docker container ls -aq) &&  
docker container rm $(docker container ls -aq) &&  
docker system prune --all --volumes
```
5. Сайт
```
http://127.0.0.1:8080
```