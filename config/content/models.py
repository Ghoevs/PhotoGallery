from django.db import models
from users.models import User


class Section(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название раздела')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Content(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='contents', verbose_name='Раздел')
    body = models.TextField(verbose_name='Содержимое')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contents', verbose_name='Автор')
    image = models.ImageField(upload_to='content/', blank=True, null=True, verbose_name='Изображение')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.TextField(verbose_name='Вопрос')
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='questions',
        null=True,
        blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name='Пользователь')
    answer = models.TextField(blank=True, null=True, verbose_name='Ответ')
    is_answered = models.BooleanField(default=False, verbose_name='Отвечен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-created_at']

    def __str__(self):
        return self.text[:50]
