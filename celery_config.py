from celery import Celery
import os
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduproject_config.settings')

app = Celery('eduapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'increment-user-life': {
        'task': 'app_accounts.tasks.increment_user_life',
        'schedule': 15.0,
    },
    'reset-day-streak-at-midnight': {
        'task': 'app_accounts.tasks.reset_day_streak',
        'schedule': crontab(hour=0, minute=0),
    },
}
