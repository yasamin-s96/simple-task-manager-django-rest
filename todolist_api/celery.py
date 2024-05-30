from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todolist_api.settings")

app = Celery("todolist_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
