from pyexpat.errors import messages

import requests
from core.config import settings
from models.notification import Notification
from models.notification_auth import NotificationAuth
from sqlalchemy.orm import Session
from db.notifications import set_provider
from models.user import User


def send_message(chat_id, message):
    TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN

    if not TELEGRAM_BOT_TOKEN:
        return True

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=data)
    return response.json()

def send_telegram_notification(db: Session, notification: Notification):
    provider = db.query(NotificationAuth).filter(
        NotificationAuth.user_id == notification.user_id,
        NotificationAuth.method == 'telegram').first()

    if not provider:
        return True

    chat_id = provider.endpoint

    return send_message(chat_id, notification.message)


def set_telegram_webhook():

    if not settings.TELEGRAM_BOT_TOKEN:
        return False

    if not settings.SERVER_HOST:
        return False

    webhook_url = f"{settings.SERVER_HOST}/telegram/webhook/{NotificationAuth.get_telegram_webhook_url_hash()}"

    # Формируем URL для запроса к Telegram API
    telegram_api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"

    # Данные для отправки в Telegram API
    payload = {
        "url": webhook_url,
    }

    # Отправляем POST-запрос для установки вебхука
    response = requests.post(telegram_api_url, json=payload)

    # Проверяем статус ответа
    if response.status_code == 200 and response.json().get("ok"):
        print("Webhook успешно установлен:", webhook_url)
        return True
    else:
        print("Ошибка при установке вебхука:", response.text)
        return False


def handle_telegram_webhook(db, data):
    """
        Обработка входящих данных от Telegram.
        """
    # Извлекаем информацию о сообщении
    message = data.get("message")
    if not message:
        print("Нет данных о сообщении.")
        return {"status": "error", "message": "No message data"}

    # Извлекаем текст сообщения
    text = message.get("text")
    if not text:
        print("Сообщение не содержит текста.")
        return {"status": "error", "message": "No text in message"}

    chat_id = message.get('chat').get('id')

    # Разделяем команду и данные
    parts = text.split(maxsplit=1)
    command = parts[0]  # Команда (например, "/auth")
    data = parts[1] if len(parts) > 1 else None  # Дополнительные данные (если есть)

    # Обработка команды
    if command == "/auth":
        if data:
            print(f"Получен код авторизации: {data}")
            user_id = NotificationAuth.check_telegram_auth_code(data)

            if user_id:
                user = db.query(User).filter(User.id==user_id).first()
                set_provider(db, user, 'telegram', chat_id)

                message =  f'You are logged in as "{user.login}"'
                send_message(chat_id, message)
                return {"status": "success", "message": f"User #{user_id} authenticated"}
            else:

                message = 'Auth code not found or expired'
                send_message(chat_id, message)
                return {'status':"error", "message":message}
        else:
            print("Команда /auth без данных.")
    elif command == "/start":
        print("Пользователь запустил бота.")

    else:
        print(f"Неизвестная команда: {command}")

    return {"status": "success", "message": "Webhook processed"}