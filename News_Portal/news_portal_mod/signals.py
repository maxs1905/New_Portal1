from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, PostCategory
from django.contrib.auth.models import User
from django.conf import settings

@receiver(post_save, sender=User)
def send_welome_email(sender, instance, created, **kwargs):
    if created:
        html_content = render_to_string('welcome.html', {'user':instance},)
        send_mail(
            subject="Добро пожаловать на сайт",
            message="Спасибо за регистрацию",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            html_message=html_content,
        )

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