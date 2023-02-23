import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Category


def weekly_posts():
    tomorrow = datetime.date.today() + datetime.timedelta(1)
    week_ago = tomorrow - datetime.timedelta(7)
    for cat in Category.objects.all():
        recepients = list(cat.subscribers.all().values('email'))
        if recepients:
            post_list = list(cat.post_set.filter(date__range=(week_ago, tomorrow)))
            html_content = render_to_string(
                'email/weekly_posts.html',
                {
                    'category': cat.name,
                    'post_list': post_list
                }
            )
            msg = EmailMultiAlternatives(
                subject='Еженедельная рассылка',
                body=f'Здравствуйте! Присылаем вам все объяления, опубликованные на прошедшей неделе в категории '
                     f'"{cat.name}": {", ".join([str(post) for post in post_list])}',
                to=[address['email'] for address in recepients]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
