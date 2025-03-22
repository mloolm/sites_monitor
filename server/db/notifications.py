from pyexpat.errors import messages
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import desc
from math import ceil
from models.notification_auth import NotificationAuth
from models.notification import Notification
from core.config import settings
from models.user import User
from sqlalchemy.exc import IntegrityError
from typing import Optional
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

def add_notification(db: Session, user: User, message: str, url:Optional[str] = None,  title:Optional[str] = None):
    db_notification = Notification(message=message, user_id=user.id, url=url, title=title)
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

def get_total_pages(db: Session, user: User, on_page: int = 30):
    total_notifications = db.query(Notification).filter(Notification.user_id == user.id).count()
    total_pages = ceil(total_notifications / on_page)
    return total_pages

def get_notifications(db: Session, user: User, page: int = 1, on_page: int = 30):
    """
    Получает уведомления для пользователя с пагинацией и сортировкой по дате создания.

    :param db: Сессия базы данных.
    :param user: Объект пользователя (User).
    :param page: Номер текущей страницы (по умолчанию 1).
    :param on_page: Количество элементов на странице (по умолчанию 30).
    """

    page = int(page)

    # Выполняем запрос с пагинацией и сортировкой по created_at (от самых ранних к самым поздним)
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc())
        .offset((page - 1) * on_page)
        .limit(on_page)
        .all()
    )

    return notifications

