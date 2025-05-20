import os
from datetime import timedelta

from celery import Celery
from celery.signals import setup_logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MonTool.settings")

app=Celery("celery_app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(["celery_tasks"])

app.conf.beat_schedule = {
    "connection_quality": {"task": "celery_tasks.tasks.connection_quality",
                  "schedule": timedelta(minutes=1)},
}

@setup_logging.connect
def configure_logging(*args, **kwargs):
    """
    Configure the logging of celery events.
    """
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)
