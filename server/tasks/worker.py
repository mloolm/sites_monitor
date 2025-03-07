# server/tasks/worker.py
from celery import Celery
from core.config import settings

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
    task_routes={
        'check_site_availability': {'queue': 'monitoring'},
        'check_ssl_certificates': {'queue': 'ssl_checks'}
    }
)