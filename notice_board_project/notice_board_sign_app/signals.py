from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives

from .models import OneTimeCode


@receiver(post_save, sender=OneTimeCode)
def send_otc(sender, instance, **kwargs):
    code = instance.code
    address = instance.user.email
    msg = EmailMultiAlternatives(
        subject='Активация аккаунта',
        body=f'Здравствуйте! Ваш аккаунт успешно создан, но чтобы активировать его перейдите по прилагаемой ссылке и '
             f'введите присланный в данном письме код.\nСсылка: http://127.0.0.1:8000/sign/signin/confirm\nКод: {code}',
        to=[address]
    )
    msg.send()
