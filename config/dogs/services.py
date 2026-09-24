from django.core.mail import send_mail
from django.conf import settings


def send_views_notification(photo):
    if photo.owner and photo.views % 20 == 0 and photo.views > 0:
        subject = f'Поздравляем! "{photo.title}" набрал {photo.views} просмотров'
        message = (
            f'Ваша фотография "{photo.title}" достигла {photo.views} просмотров!\n\n'
            f'Категория: {photo.category.name}\n\n'
            f'С уважением, Фотогалерея.'
        )
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [photo.owner.email],
            fail_silently=False,
        )