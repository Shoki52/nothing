# Выбор менее прожорливого образа
FROM python:3.10-slim-bullseye
# Создание рабочей директории
WORKDIR /code
# Копирование зависимостей
COPY ./requirements.txt /code/requirements.txt
# Обновление инструментов
RUN pip install --no-cache-dir --upgrade setuptools
# Установка зависимостей
RUN pip install -r /code/requirements.txt
# Копирование файлов
COPY . .