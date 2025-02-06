from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post, PostCategory
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from celery import shared_task


@shared_task
def send_new_post(pk):
    post=Post.objects.get(pk=pk)
    categories = post.category_post.all()
    for category in categories:
        subscribers = category.subscribers.all()
        if subscribers.exists():
            for subscriber in subscribers:
                 html_content = render_to_string(
                    'notification_created.html',
                     {
                         'post': post,
                         'subscriber': subscriber,
                         'link': settings.SITE_URL + post.get_absolute_url(),
                     }
                 )
                 msg = EmailMultiAlternatives(
                    subject=post.title_post,
                    body=f"Здравствуй, {{subscriber.username}}. Новая статья в твоём любимом разделе!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                 )
                 msg.attach_alternative(html_content, 'text/html')
                 msg.send()
@shared_task
def send_weekly_new_post():
    last_week = timezone.now() - timedelta(days=7)
    new_posts = Post.objects.filter(create_time__gte=last_week)
    subscribers = User.objects.filter(subscribers_categories__in=new_posts.values('category_post'))

    for subscriber in subscribers:
        subscribed_posts = new_posts.filter(category_post__subscribers=subscriber)
        html_content = render_to_string(
            'weekly_notification_created.html',
                {
                 'subscriber': subscriber,
                 'posts': subscribed_posts,
                 'link': settings.SITE_URL,
             }
        )

        msg = EmailMultiAlternatives(
            subject="Ваши новости за неделю",
            body=f"Здравствуй, {{ subscriber.username }}. Вот список новых статей за последнюю неделю.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()