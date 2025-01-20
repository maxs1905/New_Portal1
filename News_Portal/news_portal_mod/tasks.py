from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import timedelta
from .models import Post, Category
from django.conf import settings
from django.utils.timezone import now

def send_weekly_newsletter():
    week_ago = now() - timedelta(days=7)
    for category in Category.objects.all():
        subscribers = category.subscribers.all()

        if subscribers.exists():
            new_posts = Post.objects.filter(
                category_post=category,
                create_time__gte=week_ago
            )
            if new_posts.exists():
                for subscriber in subscribers:
                    html_content = render_to_string(
                        'weekly_newsletter.html',
                        {'posts': new_posts, 'user': subscriber}
                    )
                    msg = EmailMultiAlternatives(
                        subject=f"Новые статьи за неделю в категории '{category.name_category}'",
                        body=f"Привет, {subscriber.username}. Вот новые статьи за последнюю неделю в твоей любимой категории!",
                        from_email=settings.DEFAULT_FROM_EMAIL,  # Письмо от этого адреса
                        to=[subscriber.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()