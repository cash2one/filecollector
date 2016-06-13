import os,multiprocessing
bind = "0.0.0.0:8888"
workers = multiprocessing.cpu_count()*2 + 1
worker_class = "sync"
backlog = 2048
reload = True
debug = True
timeout = 120
