bind = "127.0.0.1:5000"          
workers = 3                      
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

loglevel = "info"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
capture_output = True