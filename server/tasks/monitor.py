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
        def check_site():
            try:
                start_time = time.time()
                response = requests.get(site.url, timeout=10)
                end_time = time.time()

                check_status_code = response.status_code
                check_is_online = 200 <= check_status_code < 300
                check_response_time_ms = round((end_time - start_time) * 1000)
            except requests.exceptions.RequestException:
                check_is_online = False
                check_status_code = None
                check_response_time_ms = None

            return check_is_online, check_status_code, check_response_time_ms

        is_online, status_code, response_time_ms = check_site()

        # Check again, to be sure
        if not is_online:
            time.sleep(5)
            is_online, status_code, response_time_ms = check_site()

        # Updates the data in the Site table.
        site.last_checked = datetime.utcnow()
        db.add(site)

        # Gets the last monitoring record for comparison.
        last_monitor_record = db.query(Monitor).filter_by(site_id=site.id).order_by(Monitor.check_dt.desc()).first()
        status_changed = False

        if last_monitor_record:
            # Checks if the status has changed.
            if last_monitor_record.is_ok != is_online:
                status_changed = True
        elif not is_online:
            status_changed = True

        # Creates a record in the Monitor table.
        monitor_record = Monitor(
            site_id=site.id,
            is_ok=is_online,
            check_dt=datetime.utcnow(),
            code=status_code,
            response_time_ms=response_time_ms
        )
        db.add(monitor_record)

        # Aggregate data
        aggregate_monitor_data(db)

        # Notification
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

    db.commit()
    db.close()

def clean_up():
    # Threshold value: records older than this period will be deleted.
    retention_period_days = 7  # 7 дней

    db: Session = SessionLocal()

    try:
        # Calculates the date until which the records are considered "old."
        cutoff_date = datetime.utcnow() - timedelta(days=retention_period_days)

        # Deletes records older than the `cutoff_date`.
        deleted_count = db.query(Monitor).filter(
            Monitor.check_dt < cutoff_date
        ).delete()

        db.commit()

        print(f"Deleted {deleted_count} records from the Monitor table.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred during cleanup: {e}")
    finally:
        db.close()