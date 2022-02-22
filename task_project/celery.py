from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_project.settings')

from django.conf import settings

app = Celery('task_project')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send_report_every_hour': {
        'task': 'users.tasks.send_requests_count',
        'schedule': crontab(hour=1),
    },
}

