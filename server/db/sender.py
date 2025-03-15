from sqlalchemy.orm import Session
from models.notification_auth import NotificationAuth
from models.notification import Notification
from core.config import settings
from services.notification_providers.telegram import send_telegram_notification
from models.user import User
from sqlalchemy.exc import IntegrityError
import json
import requests
from pywebpush import webpush, WebPushException
from pwa.pwa_manager import PwaManager
from db.notifications import get_user_notification_endpoints

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN

def send_message(db: Session, notification: Notification):
    user_id = notification.user_id

    providers = get_user_notification_endpoints(db, user_id)
    notification_send = False
    if not providers:
        return False

    for provider in providers:
        if provider['provider'] == 'telegram':
            if TELEGRAM_BOT_TOKEN:
                if send_telegram_notification(db, notification):
                    notification_send = True
        elif provider['provider'] == 'pwa':
            endpoint = json.loads(provider['endpoint'])
            if all(k in endpoint for k in ["endpoint", "keys"]) or not all(k in endpoint["keys"] for k in ["p256dh", "auth"]):

                icon = None
                url = None
                VAPID_PRIVATE_KEY = PwaManager.get_private_key()
                VAPID_CLAIMS = {
                    "sub": "mailto:" + settings.CLAIMS_EMAIL
                }

                try:
                    payload = {
                        "title": 'New event',
                        "body": notification.message,
                        "icon": icon,
                        "url": url
                    }

                    subscription_info = {
                        "endpoint": endpoint["endpoint"],
                        "keys": endpoint["keys"]
                    }

                    res = webpush(
                        subscription_info,
                        data=json.dumps(payload),
                        vapid_private_key=VAPID_PRIVATE_KEY,
                        vapid_claims=VAPID_CLAIMS
                    )


                    print(subscription_info,
                        json.dumps(payload),
                        VAPID_PRIVATE_KEY,
                        VAPID_CLAIMS,
                          res)

                    print(f"пуш-уведомления: {payload}:", res, flush=True)
                    notification_send = True
                except WebPushException as ex:

                    print(f"Ошибка отправки пуш-уведомления: {ex} {ex.response.status_code}", flush=True)
                    if ex.response.status_code in [404, 410, 401]:
                        # The subscription is no longer valid. Delete from DB
                        row = db.query(NotificationAuth).filter(NotificationAuth.id == provider['provider_id']).first()
                        if not row is None:
                            db.delete(row)  # Удаляем запись
                            db.commit()

        else:
            raise "BAD DATA"


    if notification_send:
        notification.sent = True
        db.commit()

    return True