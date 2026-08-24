from django.core.mail import send_mail
from django.conf import settings


def send_views_notification(dog):
    if dog.owner and dog.views % 20 == 0 and dog.views > 0:
        subject = f'Поздравляем! {dog.name} набрал {dog.views} просмотров'
        message = (
            f'Ваша собака {dog.name} достигла {dog.views} просмотров!\n\n'
            f'Порода: {dog.breed.name}\n'
            f'Возраст: {dog.age} лет\n\n'
            f'С уважением, Питомник.'
        )
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [dog.owner.email],
            fail_silently=False,
        )
