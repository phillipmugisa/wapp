from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Schedule the task to run every minute
app.conf.beat_schedule = {
    'run-every-minute-task': {
        'task': 'myapp.tasks.my_task',
        'schedule': 60.0,  # 60 seconds (1 minute)
    },
}