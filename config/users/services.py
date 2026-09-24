from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user):
    subject = f'Добро пожаловать, {user.username}!'
    message = f'Спасибо за регистрацию в фотогалерее!\n\nВаш email: {user.email}'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def send_password_change_email(user):
    subject = 'Пароль изменен'
    message = 'Ваш пароль был успешно изменен.'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def send_photo_created_email(user, photo):
    subject = 'Новая фотография добавлена'
    message = f'Вы добавили фотографию: {photo.title}\nКатегория: {photo.category.name}'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )