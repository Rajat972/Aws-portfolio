# Gunicorn Production Configuration for AWS EC2

bind = "0.0.0.0:8000"
workers = 3
worker_class = "sync"
keepalive = 65
timeout = 120
loglevel = "info"
accesslog = "-"
errorlog = "-"
