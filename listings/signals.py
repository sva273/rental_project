from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Listing


def send_console_mail(subject, message, recipient_list):
    """
    Отправка письма с корректной кодировкой UTF-8, чтобы Subject отображался нормально в консоли.
    """
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )
    email.encoding = 'utf-8'
    email.send()


@receiver(post_save, sender=Listing)
def listing_created_or_updated(sender, instance, created, **kwargs):
    update_fields = kwargs.get('update_fields')

    # Если создано — всегда отправляем
    if created:
        subject = f'Новое объявление создано: {instance.title}'
        message = f'Ваше объявление \"{instance.title}\" успешно размещено.'
        send_console_mail(subject, message, [instance.landlord.email])
        return

    # Если обновлялось только поле views_count — не отправляем письмо
    if update_fields is not None and update_fields == {'views_count'}:
        return

    # Иначе — считаем, что это значимое обновление
    subject = f'Объявление обновлено: {instance.title}'
    message = f'Ваше объявление \"{instance.title}\" было обновлено.'
    send_console_mail(subject, message, [instance.landlord.email])

