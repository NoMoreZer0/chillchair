import multiprocessing
import os

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
name = "chillchair"
worker_class = "gevent"

if os.environ.get("CONTAINER_ENVIRONMENT") in ["local"]:
    reload = True
    workers = 2
else:
    preload = True
    workers = multiprocessing.cpu_count()
    threads = workers
    timeout = 30
    max_requests = 3000
    max_request_jitter = 50