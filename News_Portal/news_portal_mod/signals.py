from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .views import SubscribeView
@receiver(post_save, sender=Post)
def send_newsletter(sender, instance, created, **kwargs):
    if created:
        for category in instance.category_post.all():
            for subscriber in category.subscribers.all():
                html_content = render_to_string(
                    'notification_created.html',
                    {
                        'post': instance,
                        'user': subscriber
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=instance.title_post,
                    body=f"Здравствуй, {{subscriber.username}}. Новая статья в твоём любимом разделе!",
                    from_email='Maxs.defmail@yandex.ru',
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()