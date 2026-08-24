from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('breeder', 'Заводчик'),
        ('moderator', 'Модератор'),
    ]

    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='О себе'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email
