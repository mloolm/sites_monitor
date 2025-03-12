# server/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.crud import create_site, get_site, get_sites, get_user_by_login, delete_site
from db.notifications import get_user_notification_endpoints, send_message, add_notification
from schemas.site import SiteCreate, SiteDelete, Site as SiteSchema
from schemas.user import User as UserSchema
from typing import List
from .auth import get_current_user
from models.notification import Notification
from schemas.notification import NotificationCreate, NotificationResponse, SendMessage
from services.notification_providers.telegram import send_telegram_notification
from core.config import settings
from models.notification_auth import NotificationAuth
from models.user import User

router = APIRouter(
    dependencies=[Depends(get_current_user)]  # Применяем ко всем маршрутам
)

@router.get("/user-data", response_model=UserSchema)
def get_user_data(
    current_user: str = Depends(get_current_user),  # Получаем текущего пользователя
    db: Session = Depends(get_db)
):
    """
    Возвращает информацию о текущем пользователе.
    """
    if current_user:
        return current_user
    else:
        raise HTTPException(status_code=401, detail="User not authorised")


@router.get("/get-telegram-auth-code")
def get_telegram_auth_code(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authorised")

    return NotificationAuth.get_telegram_auth_code(user_id=current_user.id)

@router.get("/user-noty-providers")
def get_user_noty(
    current_user: User = Depends(get_current_user),  # Получаем текущего пользователя
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authorised")

    providers_available = {
        'telegram': False
    }

    if settings.TELEGRAM_BOT_TOKEN:
        providers_available['telegram'] = True

    return {
        'providers':get_user_notification_endpoints(db=db, user_id=current_user.id),
        'providers_available':providers_available,

    }


@router.post("/noty-message")
def send_message_from_client(
        message: SendMessage,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):

    notification = add_notification(db, current_user, message.message)
    res = send_message(db, notification)

    if res:
        return True

    return False


@router.post("/add-site", response_model=SiteSchema)
def create_new_site(site: SiteCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return create_site(db=db, user=current_user, url=site.url)

@router.get("/sites/", response_model=List[SiteSchema])
def sites_list(db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    """
        Возвращает список всех сайтов.
        """
    sites = get_sites(db, current_user)
    if not sites:
        raise HTTPException(status_code=404, detail="No sites found")

    return sites
    #return [{"id": site.id, "url": site.url} for site in sites]
@router.get("/sites/{site_id}", response_model=SiteSchema)
def read_site(site_id: int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    db_site = get_site(db, user=current_user, site_id=site_id)
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site

@router.post("/delete-site")
def del_site(site: SiteDelete, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    res = delete_site(db, user=current_user, site_id=site.site_id)
    if not res:
        raise HTTPException(status_code=404, detail="Site not found")
    return True




@router.post("/notifications-test", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    # Отправка через Telegram, если указаны параметры

    if settings.TELEGRAM_BOT_TOKEN:
        send_telegram_notification(notification)

    return db_notification
