from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoShop.settings')

from django.conf import settings  # noqa

app = Celery('djangoShop')


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'delete-all-evening': {
        'task': 'shop.tasks.delete_all_returns',
        'schedule': crontab(hour=18),
    },
}
app.conf.timezone = 'Europe/Kiev'