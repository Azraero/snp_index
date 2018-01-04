from __future__ import absolute_import
from celery import Celery

app = Celery('clear_wroker', include=['clear_worker.tasks'])
app.config_from_object('clear_worker.config')

if __name__ == '__main__':
    app.start()
