import os
from django.core.management.base import BaseCommand
from config.users.models import User


class Command(BaseCommand):
    help = 'Создание суперпользователя'

    def handle(self, *args, **kwargs):
        email = os.getenv('SUPERUSER_EMAIL')
        password = os.getenv('SUPERUSER_PASSWORD')

        if not email or not password:
            self.stdout.write(
                self.style.ERROR(
                    'SUPERUSER_EMAIL и SUPERUSER_PASSWORD должны быть указаны в .env файле'
                )
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'Суперпользователь с email {email} уже существует')
            )
            return

        User.objects.create_superuser(
            email=email,
            username='admin',
            password=password
        )
        self.stdout.write(
            self.style.SUCCESS(f'Суперпользователь {email} успешно создан')
        )
