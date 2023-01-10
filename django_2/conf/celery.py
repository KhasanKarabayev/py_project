import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('conf')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Запуск задач по расписанию
app.conf.beat_schedule = {
    'send-email-every-5-minute': {
        'task': 'shop.tasks.send_spam',
        'schedule': crontab(minute='*/5'),

    },

}
