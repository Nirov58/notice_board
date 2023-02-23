from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from guardian.shortcuts import assign_perm
from .models import Post, Response


@receiver(post_save, sender=Post)
def author_assign_perms(sender, instance, created, **kwargs):
    if created:
        author = instance.author
        print(author)
        assign_perm('change_post', author, instance)
        assign_perm('delete_post', author, instance)


@receiver(post_save, sender=Response)
def send_response_notification(sender, instance, created, **kwargs):
    target = instance.target.name
    author = instance.author
    text = instance.text
    post_author = instance.target.author
    if created:
        assign_perm('change_response', post_author, instance)
        assign_perm('delete_response', post_author, instance)
        address = instance.target.author.email
        subject = 'Отклик на ваше объявление'
        body = f'Здравствуйте! На ваше объявление "{target}" откликнулся пользователь {author}:\n{text}.\nЧтобы ' \
               f'принять или отклонить этот отклик, а также посмотреть остальные, перейдите по ссылке: ' \
               f'http://127.0.0.1:8000/responses/'
        html_content = render_to_string(
            'email/response.html',
            {
                'target': target,
                'author': author,
                'text': text
            }
        )
    elif instance.is_accepted:
        address = instance.author.email
        subject = 'Ответ на ваш отклик'
        body = f'Здравствуйте! Ваш отклик на объявление "{target}" пользователя {post_author.username} был принят!' \
               f'\n\nХотите создать своё объяление или откликнуться на чьё-либо ещё? Зайдите в свой профиль: ' \
               f'http://127.0.0.1:8000/responses/'
    msg = EmailMultiAlternatives(
        subject=subject,
        body=body,
        to=[address]
    )
    if created:
        msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(pre_delete, sender=Response)
def send_response_rejection(sender, instance, **kwargs):
    if not instance.is_accepted:
        target = instance.target.name
        author = instance.author
        address = instance.author.email
        msg = EmailMultiAlternatives(
            subject='Ответ на ваш отклик',
            body=f'Здравствуйте! Ваш отклик на объявление {target} пользователя {author} был отклонён.\n\nХотите '
                 f'создать своё объяление или откликнуться на чьё-либо ещё? Зайдите в свой профиль: '
                 f'http://127.0.0.1:8000/responses/',
            to=[address]
        )
        msg.send()
