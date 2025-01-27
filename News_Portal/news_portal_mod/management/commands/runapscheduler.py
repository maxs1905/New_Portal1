import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from news_portal_mod.tasks import send_weekly_newsletter
from apscheduler.triggers.interval import IntervalTrigger
from django.utils.timezone import now
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        scheduler.add_job(
            send_weekly_newsletter,
            trigger=IntervalTrigger(weeks=1),
            next_run_time=now(),
            id='weekly_newslatter',
            name='Send weekly_newslatter',
            replace_existing=True
        )
        scheduler.start()
