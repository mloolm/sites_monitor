# server/tasks/monitor.py
import requests
from celery import Celery
from db.session import SessionLocal
from models.site import Site
from models.monitor import Monitor
from datetime import datetime
from core.config import settings
from sqlalchemy.orm import Session
from db.notifications import add_notification
from db.sender import send_message
from models.user import User

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

        # Получаем последнюю запись мониторинга для сравнения
        last_monitor_record = db.query(Monitor).filter_by(site_id=site.id).order_by(Monitor.check_dt.desc()).first()
        status_changed = False

        if last_monitor_record:
            # Проверяем, изменился ли статус
            if last_monitor_record.is_ok != is_online:
                status_changed = True
        elif not is_online:
            status_changed = True

        # Создаем запись в таблице Monitor
        monitor_record = Monitor(
            site_id=site.id,
            is_ok=is_online,
            check_dt=datetime.utcnow(),
            code=status_code,
        )
        db.add(monitor_record)

        # Уведомления
        if status_changed:
            if is_online:
                message = f"Site {site.url} is now online"
            else:
                message = f"Attention! Site {site.url} is offline"

            user = db.query(User).filter(User.id == site.user_id).first()
            if user:
                notification = add_notification(db, user, message)
                send_message(db, notification)

    # Сохраняем все изменения в базу данных
    db.commit()
    db.close()
