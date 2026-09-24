from django.db import models
from users.models import User
from dogs.models import Photo


class Chat(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='chats', verbose_name='Фотография')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_buyer', verbose_name='Покупатель')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_seller', verbose_name='Продавец')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        unique_together = ('photo', 'buyer')

    def __str__(self):
        return f'Чат по {self.photo.title}: {self.buyer} ↔ {self.seller}'

    def last_message(self):
        return self.messages.order_by('-created_at').first()

    def unread_count_for(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', verbose_name='Чат')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='Отправитель')
    text = models.TextField(verbose_name='Сообщение')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender}: {self.text[:30]}'