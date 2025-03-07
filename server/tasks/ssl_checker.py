# server/tasks/ssl_checker.py
import ssl
import socket
from datetime import datetime
from celery import Celery
from models.ssl_certificate import SSLCertificate
from db.session import SessionLocal

celery_app = Celery(__name__, broker=settings.REDIS_URL)


@celery_app.task
def check_ssl_certificates():
    db = SessionLocal()
    sites = db.query(Site).filter_by(is_active=True).all()

    for site in sites:
        try:
            context = ssl.create_default_context()
            with socket.create_connection((site.url, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=site.url) as ssock:
                    cert = ssock.getpeercert()

            valid_from = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
            valid_to = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')

            # Сохраняем информацию о сертификате
            ssl_cert = SSLCertificate(
                site_id=site.id,
                valid_from=valid_from,
                valid_to=valid_to,
                issuer=cert['issuer']
            )
            db.add(ssl_cert)
            db.commit()
        except Exception as e:
            print(f"SSL check failed for {site.url}: {str(e)}")