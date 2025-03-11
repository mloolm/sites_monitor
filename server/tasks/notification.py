from sqlalchemy.orm import Session
from database import SessionLocal
from models.notification import Notification
from db.notifications import send_message


def process_pending_notifications():
    db: Session = SessionLocal()
    notifications = db.query(Notification).filter(Notification.sent == False).all()


    for notification in notifications:
        send_message(db, )

    db.close()
