# server/tasks/monitor.py
import requests
from celery import Celery
from db.session import SessionLocal
from models.site import Site
from models.monitor import Monitor
from datetime import datetime
from core.config import settings
from sqlalchemy.orm import Session

celery_app = Celery(__name__, broker=settings.REDIS_URL)


@celery_app.task
def check_site_availability():
    db: Session = SessionLocal()
    sites = db.query(Site).filter_by(is_active=True).all()

    for site in sites:
        try:

            response = requests.get(site.url, timeout=10)
            status_code = response.status_code
            is_online = 200 <= status_code < 300
        except requests.exceptions.RequestException:
            is_online = False
            status_code = None

        # Обновляем данные в таблице Site
        site.last_checked = datetime.utcnow()
        db.add(site)

        # Создаем запись в таблице Monitor
        monitor_record = Monitor(
            site_id=site.id,
            is_ok=is_online,
            check_dt=datetime.utcnow(),
            code=status_code,
        )
        db.add(monitor_record)

    # Сохраняем все изменения в базу данных
    db.commit()
    db.close()