from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('breeder', 'Заводчик'),
        ('moderator', 'Модератор'),
    ]

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, null=True, verbose_name='О себе')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', verbose_name='Роль')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    @property
    def has_subscription(self):
        if hasattr(self, 'subscription'):
            return self.subscription.is_valid()
        return False


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('month', 'На месяц'),
        ('year', 'На год'),
        ('forever', 'Навсегда'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Пользователь'
    )
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='month', verbose_name='Тариф')
    is_active = models.BooleanField(default=False, verbose_name='Активна')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Начало')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='Окончание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        status = 'активна' if self.is_active else 'неактивна'
        return f'Подписка {self.user.username} ({status})'

    def activate(self, plan='month'):
        self.plan = plan
        self.is_active = True
        self.started_at = timezone.now()
        if plan == 'month':
            self.expires_at = timezone.now() + timedelta(days=30)
        elif plan == 'year':
            self.expires_at = timezone.now() + timedelta(days=365)
        else:
            self.expires_at = None
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            self.is_active = False
            self.save()
            return False
        return True