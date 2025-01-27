import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')

app = Celery('News_Portal')
app.conf.beat_shedule = {
    'send-weekly-newsletter': {'task': 'news.tasks.send-weekly-newsletter', 'schedule': crontab(hour=8, minute=0, day_of_week=1),}
}
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()