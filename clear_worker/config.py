from datetime import timedelta
from clear_worker.tasks import CLEAR_PATH

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULE = {
    'clearwork': {
        'task': 'clear_worker.tasks.ClearWorker',
        'schedule': timedelta(days=1),
        'args': (CLEAR_PATH,)
    },
}
