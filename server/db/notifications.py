from typing import List, Dict
from sqlalchemy.orm import Session
from math import ceil
from models.notification_auth import NotificationAuth
from models.notification import Notification
from core.config import settings
from models.user import User
from sqlalchemy.exc import IntegrityError
from typing import Optional


TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN

def get_user_notification_endpoints(db: Session, user_id: int) -> List[Dict[str, str]]:
    """
    Gets the list of notification providers and their endpoints for the specified user.

    :param db: Database session
    :param user_id: User ID
    :return: A list of dictionaries with providers and endpoints, or an empty list.
    """

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
    """Adds or updates the notification method for the user."""
    if provider not in ["telegram", "pwa"]:
        raise ValueError("Error: Invalid notification provider!")

    endpoint = str(endpoint)
    endpoint_hash = NotificationAuth.get_endpoint_hash(endpoint)
    auth_entry = db.query(NotificationAuth).filter_by(user_id=user.id, method=provider, endpoint_hash=endpoint_hash).first()

    if auth_entry:
        # If the record already exists, update the endpoint.
        auth_entry.endpoint = endpoint
    else:
        # If the record does not exist, create a new one.
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
    Gets notifications for the user with pagination and sorting by creation date.

    :param db: Database session.
    :param user: User object (User).
    :param page: Current page number (default is 1).
    :param on_page: Number of items per page (default is 30).
    """

    page = int(page)

    # Performs the query with pagination and sorting by created_at (from the earliest to the latest).
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc())
        .offset((page - 1) * on_page)
        .limit(on_page)
        .all()
    )

    return notifications