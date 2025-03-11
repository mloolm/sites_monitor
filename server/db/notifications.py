from pyexpat.errors import messages
from typing import List, Dict
from sqlalchemy.orm import Session
from models.notification_auth import NotificationAuth
from models.notification import Notification
from config import TELEGRAM_BOT_TOKEN
from services.notification_providers.telegram import send_telegram_notification


def get_user_notification_endpoints(db: Session, user_id: int) -> List[Dict[str, str]]:
    """
    Получает список провайдеров уведомлений и их endpoint для указанного пользователя.

    :param db: Сессия базы данных
    :param user_id: ID пользователя
    :return: Список словарей с провайдерами и endpoint, либо пустой список
    """
    # Запрашиваем все записи для данного пользователя
    auth_entries = (
        db.query(NotificationAuth)
        .filter(NotificationAuth.user_id == user_id)
        .all()
    )

    # Формируем список словарей с провайдерами и их endpoint
    result = [
        {"provider": entry.method, "endpoint": entry.endpoint}
        for entry in auth_entries
    ]

    return result

def send_message(db: Session, notification: Notification):
    user_id = notification.user_id

    providers = get_user_notification_endpoints(db, user_id)
    notification_send = False;
    if not providers:
        return False

    for provider in providers:
        if provider.method == 'telegram':
            if TELEGRAM_BOT_TOKEN:
                if send_telegram_notification(notification):
                    notification_send = True

    if notification_send:
        notification.sent = True
        db.commit()