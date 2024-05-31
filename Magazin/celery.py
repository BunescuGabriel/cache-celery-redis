from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Magazin.settings')

app = Celery('Magazin')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get_categories_every_one_minute': {
        'task': 'laptop.tasks.send_best_email',
        'schedule': crontab(minute='*/1'),
        # 'schedule': crontab(second='*/20'),  
    },
}
