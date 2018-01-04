from datetime import timedelta
from clear_worker.tasks import CLEAR_PATH

BROKER_URL = 'redis://localhost:6380/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6380/0'
CELERYBEAT_SCHEDULE = {
    'clearwork': {
        'task': 'clear_worker.tasks.ClearWorker',
        'schedule': timedelta(seconds=10),
        'args': (CLEAR_PATH,)
    },
}