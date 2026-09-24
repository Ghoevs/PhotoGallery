from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Photo(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Категория'
    )
    image = models.ImageField(upload_to='photos/', verbose_name='Фотография')
    description = models.TextField(blank=True, verbose_name='Описание')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='photos',
        null=True,
        blank=True,
        verbose_name='Владелец'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Цена (₽)'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return self.title


class Review(models.Model):
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Фотография'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    text = models.TextField(verbose_name='Отзыв')
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name='Оценка'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.user.username} на {self.photo.title}'