from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import send_new_post


@receiver(m2m_changed, sender=PostCategory)
def send_newsletter(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        send_new_post.delay(instance.pk)
