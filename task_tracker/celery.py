import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_tracker.settings')

app = Celery('task_tracker')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

app.conf.beat_schedule = {
    'price-update':{
        'task':'core.tasks.send_mail',
        'schedule':15,
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')