import ssl
import socket
from datetime import datetime, timedelta
from celery import shared_task
from pytz import utc
from db.session import SessionLocal
from models.site import Site
from models.ssl_certificate import SSLCertificate
from db.notifications import add_notification
from db.sender import send_message
from models.user import User
from urllib.parse import urlparse

@shared_task
def check_ssl_certificates():
    db = SessionLocal()
    sites = db.query(Site).filter_by(is_active=True).all()
    users = {}

    for site in sites:
        try:
            if not hasattr(site, 'url') or not isinstance(site.url, str):
                continue

            if not site.url:
                continue

            # Checks if the URL starts with `https://`.
            if not site.url.startswith('https://'):
                continue

            parsed_url = urlparse(site.url)
            domain = parsed_url.netloc

            if not domain:
                continue

            # Retrieves the SSL certificate.
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()

            # Parses dates.
            valid_from = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=utc)
            valid_to = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=utc)
            current_time = datetime.utcnow().replace(tzinfo=utc)

            # Checks the validity of the certificate.
            is_valid = valid_from <= current_time <= valid_to
            is_expiring_soon = (valid_to - current_time).days <= 7

            # Extracts the issuer.
            issuer = dict(x[0] for x in cert['issuer'])
            issuer_str = f"{issuer.get('organizationName', 'N/A')} ({issuer.get('commonName', 'N/A')})"

            # Creates a record in the database.
            ssl_cert = SSLCertificate(
                site_id=site.id,
                is_ok=is_valid,  
                check_dt=current_time,
                issuer=issuer_str,
                valid_from=valid_from,
                valid_to=valid_to,
            )
            db.add(ssl_cert)
            db.commit()

            # If the certificate is about to expire, notifies the user.
            if is_expiring_soon:
                message = f"Certificate for {site.url} expires in {(valid_to - current_time).days} days!"
                noty_url = '/dashboard'
                noty_title = "SSL ALERT!"

                if site.user_id not in users:
                    users[site.user_id] = db.query(User).filter(User.id == site.user_id).first()

                if site.user_id in users and users[site.user_id]:
                    notification = add_notification(db, users[site.user_id], message, noty_url, noty_title)
                    send_message(db, notification)

        except Exception as e:
            # If the certificate has expired or is invalid, makes the corresponding
            # record in the database and notifies the user.

            ssl_cert = SSLCertificate(
                site_id=site.id,
                is_ok=False,
                check_dt=datetime.utcnow().replace(tzinfo=utc),
                issuer="Error",
                valid_from=None,
                valid_to=None,
            )
            db.add(ssl_cert)
            db.commit()
            print(f"SSL check failed for {site.url}: {str(e)}")

            message = f"ALERT: SSL certificate for {site.url} is missing or invalid!"
            if site.user_id not in users:
                users[site.user_id] = db.query(User).filter(User.id == site.user_id).first()

            if site.user_id in users and users[site.user_id]:
                noty_url = '/dashboard'
                noty_title = "SSL Error!"
                notification = add_notification(db, users[site.user_id], message, noty_url, noty_title)
                send_message(db, notification)
