from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user):
    subject = f'Добро пожаловать, {user.username}!'
    message = f'Спасибо за регистрацию в нашем питомнике!\n\nВаш email: {user.email}'
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


def send_dog_created_email(user, dog):
    subject = 'Создана новая карточка собаки'
    message = f'Вы создали карточку собаки: {dog.name}\nПорода: {dog.breed.name}\nВозраст: {dog.age} лет'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
