# models/__init__.py
from .site import Site
from .user import User
from .monitor import Monitor
from .ssl_certificate import SSLCertificate
from .notification import Notification
from .notification_auth import NotificationAuth
from .monitor_by_days import MonitorByDay
# Экспортируем все модели
__all__ = [
    "Site",
    "User",
    "Monitor",
    "SSLCertificate",
    "Notification",
    "NotificationAuth",
    "MonitorByDay"
]