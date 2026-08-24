# Питомник собак — Django проект

## Описание
Web-приложение для питомника собак с функционалом регистрации, карточками собак, отзывами, родословными и API.

## Технологии
- Python 3.12
- Django 6.0
- SQL Server (MSSQL)
- Django REST Framework
- Docker

## Установка

### Локальный запуск
1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте: `venv\Scripts\activate`
4. Установите зависимости: `pip install -r requirements.txt`
5. Скопируйте `.env_sample` в `.env` и заполните
6. Выполните миграции: `python manage.py migrate`
7. Создайте суперпользователя: `python manage.py createsuperuser`
8. Запустите сервер: `cd config -> python manage.py runserver`

### Запуск в Docker
1. `docker-compose up --build`
2. `docker-compose exec web python manage.py migrate`
3. `docker-compose exec web python manage.py createsuperuser`
4. Откройте http://localhost:8000