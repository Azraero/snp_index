from __future__ import absolute_import
import os
import math
import subprocess
from clear_worker.celery import app

CLEAR_PATH = os.path.join(os.path.dirname(__file__), 'app', 'static', 'variation_results')
MAX_SIZE = 1 << 30
RM_PART = 0.3


def getdirsize(dir):
    size = 0L
    all_files = []
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        all_files += [os.path.realpath(os.path.join(root, name)) for name in files]
    return size, all_files


def compare(x, y):
    x_time = os.path.getmtime(x)
    y_time = os.path.getmtime(y)
    if x_time > y_time:
        return 1
    elif x_time == y_time:
        return 0
    else:
        return -1


@app.task
def ClearWorker(dir):
    size, all_files = getdirsize(dir)
    if size > MAX_SIZE:
        all_files.sort(compare)
    rm_number = math.ceil(RM_PART * len(all_files))
    print rm_number
    for each in all_files[:int(rm_number)]:
        subprocess.call('rm -rf {0}'.format(each), shell=True)
    return None



