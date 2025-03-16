from datetime import datetime, timedelta
from sqlalchemy import text

from models.monitor import Monitor
from sqlalchemy.orm import Session

from sqlalchemy import desc
from datetime import datetime, timedelta

def get_sites_health(db: Session, sites):
    site_ids = [site.id for site in sites]

    # Определяем дату начала последней недели
    last_week = datetime.utcnow() - timedelta(days=7)

    # SQL-запрос для подсчета проверок и доступности
    sql = text("""
        SELECT 
            site_id, 
            COUNT(*) as total_checks, 
            SUM(CASE WHEN is_ok THEN 1 ELSE 0 END) as successful_checks 
        FROM 
            monitor 
        WHERE 
            site_id IN :site_ids 
            AND check_dt > :last_week 
        GROUP BY 
            site_id
    """)

    # Выполняем запрос
    result = db.execute(sql, {"site_ids": tuple(site_ids), "last_week": last_week}).fetchall()

    # Подсчитываем процент доступности для каждого сайта
    health_data = {}
    for row in result:
        site_id = row.site_id
        total_checks = row.total_checks
        successful_checks = row.successful_checks
        availability_percentage = round((successful_checks / total_checks * 100)) if total_checks > 0 else 0
        health_data[site_id] = {
            'up':availability_percentage,
            'ssl':None
        }


    #SSL сертиикаты
    sql = text("""WITH ranked AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY site_id ORDER BY check_dt DESC) AS rn
            FROM ssl_monitor
            WHERE site_id IN :site_ids
        )
        SELECT * FROM ranked WHERE rn = 1;
          
            """)
    ssl_state = db.execute(sql, {"site_ids": tuple(site_ids)}).fetchall()
    if ssl_state:
        for row in ssl_state:
            health_data[row.site_id]['ssl'] = row.valid_to

    print (health_data)

    return health_data

def get_site_data(db: Session, site_id:int, period:str='week'):
    monitor_records = None
    if period in ['week', 'day']:
        if period == 'week':
            period = datetime.utcnow() - timedelta(days=7)
        elif period == 'day':
            period = datetime.utcnow() - timedelta(days=1)


        monitor_records = (
            db.query(Monitor)
            .filter(Monitor.site_id == site_id, Monitor.check_dt >= period)
            .order_by(Monitor.check_dt)  # Сортируем по check_dt от нового к старому
            .all()
        )
    elif period in ['month', 'year']:
        print(f"Period: {period}")

    if not monitor_records:
        return []

    # Преобразуем результаты в нужный формат
    formatted_records = [
        {
            "check_dt": monitor_record.check_dt.isoformat() + "Z",  # Преобразуем в ISO 8601 формат
            "is_ok": monitor_record.is_ok,
            "code": monitor_record.code,
            "response_time_ms": monitor_record.response_time_ms
        }
        for monitor_record in monitor_records
    ]

    return formatted_records


