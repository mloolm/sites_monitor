from pyexpat.errors import messages
from typing import List, Dict
from sqlalchemy.orm import Session
from models.notification_auth import NotificationAuth
from models.notification import Notification
from core.config import settings
from models.user import User
from sqlalchemy.exc import IntegrityError
import json
import requests
from pywebpush import webpush, WebPushException
from pwa.pwa_manager import PwaManager


TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN

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
        {"provider": entry.method, "provider_id": entry.id, "endpoint": entry.endpoint}
        for entry in auth_entries
    ]
    return result

def add_notification(db: Session, user: User, message: str):
    db_notification = Notification(message=message, user_id=user.id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification




def set_provider(db: Session, user: User, provider: str, endpoint: str):
    """Добавляет или обновляет метод уведомлений для пользователя."""
    if provider not in ["telegram", "pwa"]:
        raise ValueError("Ошибка: Недопустимый провайдер уведомлений!")

    endpoint = str(endpoint)
    endpoint_hash = NotificationAuth.get_endpoint_hash(endpoint)
    auth_entry = db.query(NotificationAuth).filter_by(user_id=user.id, method=provider, endpoint_hash=endpoint_hash).first()

    if auth_entry:
        # Если запись уже есть, обновляем endpoint
        auth_entry.endpoint = endpoint
    else:
        # Если записи нет, создаём новую
        auth_entry = NotificationAuth(user_id=user.id, method=provider, endpoint=endpoint, endpoint_hash=endpoint_hash)
        db.add(auth_entry)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return True

    return True

