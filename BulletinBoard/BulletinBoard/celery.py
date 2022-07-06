import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BulletinBoard.settings')

app = Celery('BulletinBoard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_email_to_subscribers': {
        'task': 'board.tasks.email_to_subscribers',
        'schedule': crontab()
    },
}

app.autodiscover_tasks()
