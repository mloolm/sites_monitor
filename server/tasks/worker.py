# server/tasks/worker.py
from celery import Celery
from core.config import settings
from .monitor import check_site_availability

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        "check-site-availability": {
            "task": "tasks.monitor.check_site_availability",
            "schedule": settings.INTERVAL * 60,
        },
    }
)