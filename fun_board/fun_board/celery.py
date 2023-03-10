import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fun_board.settings')

app = Celery('fun_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'posts.tasks.send_mail_to_subscriber',
        # fot production
        # 'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # for develop
        'schedule': 10,
        'args': (),
    },
}
