# file gunicorn.conf.py
# coding=utf-8
# Reference: https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
import multiprocessing

bind = '0.0.0.0:5000'
backlog = 2048
workers = multiprocessing.cpu_count() * 2 + 1

timeout = 1 * 60  # 1 minutes
keepalive = 24 * 60 * 60  # 1 day
