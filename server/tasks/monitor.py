# server/tasks/monitor.py
import requests
from celery import Celery
from db.session import SessionLocal
from models.site import Site
from models.monitor import Monitor
from datetime import datetime, timedelta
from core.config import settings
from sqlalchemy.orm import Session
from db.notifications import add_notification
from db.sender import send_message
from models.user import User
from db.monitor_by_day import aggregate_monitor_data
import time

celery_app = Celery(__name__, broker=settings.REDIS_URL)


@celery_app.task
def check_site_availability():
    db: Session = SessionLocal()
    sites = db.query(Site).filter_by(is_active=True).all()

    for site in sites:
        try:
            start_time = time.time()
            response = requests.get(site.url, timeout=10)
            end_time = time.time()

            status_code = response.status_code
            is_online = 200 <= status_code < 300
            response_time_ms = round((end_time - start_time) * 1000)
        except requests.exceptions.RequestException:
            is_online = False
            status_code = None
            response_time_ms = None

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
            response_time_ms=response_time_ms
        )
        db.add(monitor_record)

        #свертка данных
        aggregate_monitor_data(db)

        # Уведомления
        if status_changed:
            noty_url = f'/site/{site.id}'

            if is_online:
                noty_title = "Hooray!"
                message = f"Site {site.url} is now online"
            else:
                noty_title = "Attention!"
                message = f"Site {site.url} is offline"

            user = db.query(User).filter(User.id == site.user_id).first()
            if user:
                notification = add_notification(db, user, message, noty_url, noty_title)
                send_message(db, notification)

    # Сохраняем все изменения в базу данных
    db.commit()
    db.close()

def clean_up():
    # Пороговое значение: записи старше этого периода будут удалены
    retention_period_days = 7  # 7 дней

    # Создаем сессию базы данных
    db: Session = SessionLocal()

    try:
        # Вычисляем дату, до которой записи считаются "старыми"
        cutoff_date = datetime.utcnow() - timedelta(days=retention_period_days)

        # Удаляем записи старше cutoff_date
        deleted_count = db.query(Monitor).filter(
            Monitor.check_dt < cutoff_date
        ).delete()

        # Фиксируем изменения в базе данных
        db.commit()

        print(f"Deleted {deleted_count} records from the Monitor table.")
    except Exception as e:
        # В случае ошибки откатываем транзакцию
        db.rollback()
        print(f"An error occurred during cleanup: {e}")
    finally:
        # Закрываем сессию
        db.close()