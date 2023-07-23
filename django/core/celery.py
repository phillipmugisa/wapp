from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set django setting module environment variable for celery program

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core", broker=os.environ.get("CELERY_BROKER", "redis://redis:6379/0"))
app.config_from_object("django.conf:settings", namespace="CELERY")

# auto discover tasks in other apps
app.autodiscover_tasks()