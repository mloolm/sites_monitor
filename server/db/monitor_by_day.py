from datetime import datetime, timedelta
from sqlalchemy import func, case, and_, cast, Numeric
from sqlalchemy.orm import Session
from models.monitor import Monitor
from models.monitor_by_days import MonitorByDay
from decimal import Decimal

def aggregate_monitor_data(db: Session):
    today = datetime.utcnow().date()

    # Gets all websites.
    sites = db.query(Monitor.site_id).distinct().all()

    for site in sites:
        site_id = site.site_id

        # Determines the last processed day from the monitor_by_day table.
        last_processed_day = db.query(
            func.max(func.date(MonitorByDay.check_dt))
        ).filter(
            MonitorByDay.site_id == site_id
        ).scalar()

        # If there are no processed days, take the earliest date from the monitor table.
        if not last_processed_day:
            earliest_date = db.query(func.min(func.date(Monitor.check_dt))).filter(
                Monitor.site_id == site_id
            ).scalar()
            start_date = earliest_date or today
        else:
            start_date = last_processed_day + timedelta(days=1)  # Start from the next day.

        aggregated_data = db.query(
            func.date(Monitor.check_dt).label("check_date"),
            func.count().label("total_checks"),
            func.sum(case((Monitor.is_ok == True, 1), else_=0)).label("successful_checks"),
            cast(
                func.sum(case((Monitor.is_ok == True, 1), else_=0)) * 100 / func.count(),
                Numeric(precision=5, scale=2)
            ).label("uptime_percentage")
        ).filter(
            and_(
                Monitor.site_id == site_id,
                func.date(Monitor.check_dt) >= start_date,
                func.date(Monitor.check_dt) < today
            )
        ).group_by(
            func.date(Monitor.check_dt)
        ).all()

        # Inserts new data into the monitor_by_day table.
        for data in aggregated_data:
            new_record = MonitorByDay(
                site_id=site_id,
                uptime=int(data.uptime_percentage),
                check_dt=datetime.combine(data.check_date, datetime.min.time())
            )
            db.add(new_record)

    # Determines the start and end of the current day.
    start_of_today = datetime(today.year, today.month, today.day, 0, 0, 0)
    end_of_today = start_of_today + timedelta(days=1) - timedelta(seconds=1)

    # Updates data for today.
    today_data = db.query(
        Monitor.site_id,
        func.count().label("total_checks"),
        func.sum(case((Monitor.is_ok == True, 1), else_=0)).label("successful_checks")
    ).filter(
        and_(
            Monitor.check_dt >= start_of_today,
            Monitor.check_dt <= end_of_today
        )
    ).group_by(Monitor.site_id).all()

    for data in today_data:
        total_checks = Decimal(data.total_checks or Decimal(0))
        successful_checks = Decimal(data.successful_checks or Decimal(0))

        # Calculate uptime_percentage
        uptime_percentage = (successful_checks * Decimal(100) / total_checks).quantize(Decimal('0.00')) \
            if total_checks > 0 else Decimal('0.00')

        # Checks if there is a record for today.
        existing_record = db.query(MonitorByDay).filter(
            and_(
                MonitorByDay.site_id == data.site_id,
                func.date(MonitorByDay.check_dt) == today
            )
        ).first()

        if existing_record:
            # Update
            existing_record.uptime = uptime_percentage
        else:
            # Insert
            new_record = MonitorByDay(
                site_id=data.site_id,
                uptime=uptime_percentage,
                check_dt=datetime.combine(today, datetime.min.time())
            )
            db.add(new_record)

    db.commit()