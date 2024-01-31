## Установка
* Клонировать репозиторий: `git clone https://gitlab.com/13lab/sara-marketplace`
* Скачать и установить Docker и Docker-Compose: https://docs.docker.com/engine/install/
* Перейти в директорию проекта: `cd ~/sara-marketplace`
* Изменить значения аутентификации в БД и подписей JWT-токенов в файле `.env`. 
* Перейти в директорию: `~/frontend`
* Изменить значение ссылки, на которой будет находится backend в файле `.env`
* Перейти в директорию: `~/backend/nginx`
* Изменить значение `sara.13lab.tech` на домен своего сервера
* Запустить Docker Compose с помощью команды: `docker compose up -d --build`
* Зарегистрировать сертификаты на домен с помощью команды: `docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d домен_вашего_сервера`
* Выключить Docker Compose с помощью команды: `docker compose down`
* В `nginx.conf` убрать комментарии в данном месте:
```
#
# server {
#      # HTTP
#     listen 443 ssl;
#
#     # Домен или localhost
#     server_name sara.13lab.tech;
#
#     ssl_certificate /etc/nginx/ssl/live/sara.13lab.tech/fullchain.pem;
#     ssl_certificate_key /etc/nginx/ssl/live/sara.13lab.tech/privkey.pem;
#     # Backend
#     location /api/ {
#         # То куда реверс-прокси переводит запрос
#         proxy_pass http://fastapi;
#         # В логах добавляет хост, на который обратились
#         proxy_set_header Host $http_host;
#         # В логах добавляет ip-адрес обратившегося
#         proxy_set_header X-Real-IP $remote_addr;
#     }
#     # Frontend
#     location / {
#         proxy_pass http://frontend;
#  }
# }
#

```
* Вернуться в директорию проекта: `cd ~/sara-marketplace`
* Убрать комментарии в `docker-compose.yml` в данном месте:
```
  nginx:
    image: nginx:latest
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./backend/nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - ./backend/certbot/www:/var/www/certbot/
#      - ./backend/certbot/conf/:/etc/nginx/ssl/
    depends_on:
      - fastapi
    restart: on-failure
```
* Запустить Docker Compose с помощью команды: `sudo docker compose up -d --build`
* Перейти в директорию: `~/backend`
* Достать данные из бэкапа в базу данных с помощью команды: `docker exec -i postgresql psql -U postgres -d db_test < dump.sql`
* Перейти на указанный домен и проверить работает ли все