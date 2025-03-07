# server/tasks/monitor.py
import requests
from celery import Celery
from db.session import SessionLocal
from models.site import Site
from datetime import datetime

celery_app = Celery(__name__, broker=settings.REDIS_URL)


@celery_app.task
def check_site_availability():
    db = SessionLocal()
    sites = db.query(Site).filter_by(is_active=True).all()

    for site in sites:
        try:
            response = requests.get(site.url, timeout=10)
            status_code = response.status_code
            is_online = 200 <= status_code < 300
        except requests.exceptions.RequestException:
            is_online = False

        site.last_checked = datetime.utcnow()
        # Сохраняем результат в базу
        db.commit()