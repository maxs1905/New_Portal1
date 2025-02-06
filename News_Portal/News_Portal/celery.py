import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')

app = Celery('News_Portal')
app.conf.beat_schedule = {
    'send_weekly_new_post': {
        'task': 'news_portal_mod.tasks.send_weekly_new_post',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),

    }
}
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()