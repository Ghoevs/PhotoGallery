from django.db import models
from users.models import User


class Breed(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название породы')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'

    def __str__(self):
        return self.name


class Dog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Кличка')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='dogs', verbose_name='Порода')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст (лет)')
    photo = models.ImageField(upload_to='dogs/', blank=True, null=True, verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Описание')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dogs',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'
        permissions = [
            ('can_change_active', 'Может менять активность'),
            ('can_change_owner', 'Может менять владельца'),
        ]

    def __str__(self):
        return f'{self.name} ({self.breed.name})'


class Pedigree(models.Model):
    dog = models.OneToOneField(Dog, on_delete=models.CASCADE, related_name='pedigree', verbose_name='Собака')
    father = models.CharField(max_length=100, blank=True, verbose_name='Отец')
    mother = models.CharField(max_length=100, blank=True, verbose_name='Мать')
    grandfather_father = models.CharField(max_length=100, blank=True, verbose_name='Дед по отцу')
    grandmother_father = models.CharField(max_length=100, blank=True, verbose_name='Бабка по отцу')
    grandfather_mother = models.CharField(max_length=100, blank=True, verbose_name='Дед по матери')
    grandmother_mother = models.CharField(max_length=100, blank=True, verbose_name='Бабка по матери')
    awards = models.TextField(blank=True, verbose_name='Награды')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Родословная'
        verbose_name_plural = 'Родословные'

    def __str__(self):
        return f'Родословная {self.dog.name}'


class Review(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='reviews', verbose_name='Собака')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
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
        return f'Отзыв от {self.user.username} на {self.dog.name}'
