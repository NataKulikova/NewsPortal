import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'board.tasks.printer',
#         'schedule': 5,
#         'args': (5,),
#     },
# }

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'board.tasks.printer',
        'schedule': crontab(hour=17, minute=30, day_of_week='sunday'),
        'args': ("some_arg"),
    },
}