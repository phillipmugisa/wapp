from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-60-seconds': {
        'task': 'manager.tasks.send_scheduled_message',
        'schedule': 60.0,
    },
}
app.conf.timezone = 'UTC'
