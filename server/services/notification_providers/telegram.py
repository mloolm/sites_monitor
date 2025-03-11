import requests
from core.config import settings
from models.notification import Notification
from models.notification_auth import NotificationAuth
from sqlalchemy.orm import Session


def send_telegram_notification(db: Session, notification: Notification):
    chat_id = db.query(NotificationAuth).filter(
        NotificationAuth.user_id == notification.user_id,
        NotificationAuth.method == 'telegram').first()

    if not chat_id:
        return True

    TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN

    if not TELEGRAM_BOT_TOKEN:
        return True

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    message = notification.message

    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=data)
    return response.json()


def handle_telegram_webhook(db, data):
    return True