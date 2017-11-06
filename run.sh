uwsgi --http-socket 0.0.0.0:9000 --wsgi-file manager.py --callable app --processes 4 --threads 2 --stats 0.0.0.0:5000
