from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Booking, BookingStatusChoices


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


@receiver(post_save, sender=Booking)
def booking_created_or_updated(sender, instance, created, **kwargs):
    landlord_email = instance.listing.landlord.email
    tenant_email = instance.tenant.email

    if created:
        subject = f'Новое бронирование: {instance.listing.title}'
        message_tenant = f'Вы забронировали "{instance.listing.title}". Ожидайте подтверждения.'
        message_landlord = f'Ваш объект "{instance.listing.title}" был забронирован.'
        send_console_mail(subject, message_tenant, [tenant_email])
        send_console_mail(subject, message_landlord, [landlord_email])
    else:
        if instance.status == BookingStatusChoices.CONFIRMED:
            subject = f'Бронирование подтверждено: {instance.listing.title}'
            message = f'Бронирование "{instance.listing.title}" подтверждено.'
            send_console_mail(subject, message, [tenant_email, landlord_email])
        elif instance.status == BookingStatusChoices.REJECTED:
            subject = f'Бронирование отклонено: {instance.listing.title}'
            message = f'Бронирование "{instance.listing.title}" отклонено.'
            send_console_mail(subject, message, [tenant_email, landlord_email])


@receiver(post_delete, sender=Booking)
def booking_deleted(sender, instance, **kwargs):
    landlord_email = instance.listing.landlord.email
    tenant_email = instance.tenant.email
    subject = f'Бронирование удалено: {instance.listing.title}'
    message = f'Бронирование "{instance.listing.title}" было удалено.'
    send_console_mail(subject, message, [tenant_email, landlord_email])
