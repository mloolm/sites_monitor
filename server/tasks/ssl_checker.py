# server/tasks/ssl_checker.py
import ssl
import socket
from datetime import datetime, timedelta
from celery import shared_task
from pytz import utc
from db.session import SessionLocal
from models.site import Site
from models.ssl_certificate import SSLCertificate


@shared_task
def check_ssl_certificates():
    db = SessionLocal()
    sites = db.query(Site).filter_by(is_active=True).all()

    for site in sites:
        try:
            # Извлекаем домен из URL
            domain = site.url.replace("http://", "").replace("https://", "").split('/')[0]

            # Получаем SSL-сертификат
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()

            # Парсим даты
            valid_from = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=utc)
            valid_to = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=utc)
            current_time = datetime.utcnow().replace(tzinfo=utc)

            # Проверка валидности сертификата
            is_valid = valid_from <= current_time <= valid_to
            is_expiring_soon = (valid_to - current_time).days <= 7

            # Извлекаем издателя
            issuer = dict(x[0] for x in cert['issuer'])
            issuer_str = f"{issuer.get('organizationName', 'N/A')} ({issuer.get('commonName', 'N/A')})"

            # Создаем запись в базе
            ssl_cert = SSLCertificate(
                site_id=site.id,
                is_ok=is_valid,  # Теперь зависит от срока действия
                check_dt=current_time,
                issuer=issuer_str,
                valid_from=valid_from,
                valid_to=valid_to,
            )
            db.add(ssl_cert)
            db.commit()

            # Уведомление о скором истечении (заглушка)
            if is_expiring_soon:
                print(f"ALERT: Certificate for {site.url} expires in {(valid_to - current_time).days} days!")

        except Exception as e:
            # Обработка ошибок
            ssl_cert = SSLCertificate(
                site_id=site.id,
                is_ok=False,
                check_dt=datetime.utcnow(),
                issuer="Error",
                valid_from=None,
                valid_to=None,
            )
            db.add(ssl_cert)
            db.commit()
            print(f"SSL check failed for {site.url}: {str(e)}")