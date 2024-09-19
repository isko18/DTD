import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_expiring_tariffs_every_first_day_of_the_month': {
        'task': 'business.tasks.check_expiring_tariffs',
        'schedule': crontab(hour=10, minute=0),
    },
    'update_tariffs_every_first_day_of_the_month': {
        'task': 'business.tasks.update_tariffs',
        'schedule': crontab(hour=0, minute=0),
    },
}
app.conf.timezone = 'Asia/Bishkek'
