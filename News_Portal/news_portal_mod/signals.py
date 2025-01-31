from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, PostCategory
from django.contrib.auth.models import User
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


@receiver(m2m_changed, sender=PostCategory)
def send_newsletter(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
         categories = instance.category_post.all()
         for category in categories:
             subscribers = category.subscribers.all()
             if subscribers.exists():
                for subscriber in subscribers:
                    html_content = render_to_string(
                        'notification_created.html',
                        {
                            'post': instance,
                            'subscriber': subscriber
                        }
                    )

                    msg = EmailMultiAlternatives(
                        subject=instance.title_post,
                        body=f"Здравствуй, {{subscriber.username}}. Новая статья в твоём любимом разделе!",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[subscriber.email],
                    )
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send()
@receiver(m2m_changed, sender=PostCategory)
def send_weekly_newsletter(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        last_week = timezone.now() - timedelta(days=7)
        new_posts = Post.objects.filter(create_time__gte=last_week)
        subscribers = User.objects.filter(subscribers__in=new_posts.values('category_post'))

        for subscriber in subscribers:
            subscribed_posts = new_posts.filter(category_post__subscribers=subscriber)
            html_content = render_to_string(
                'weekly_notification_created.html',
                {
                    'subscriber': subscriber,
                    'posts': subscribed_posts,
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
