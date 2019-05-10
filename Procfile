web: gunicorn mxv.wsgi --timeout 300
worker: ./manage.py rqworker default
scheduler: ./manage.py rqscheduler --interval 1
release: ./manage.py migrate
