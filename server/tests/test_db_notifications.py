import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from models.notification_auth import NotificationAuth
from models.notification import Notification
from models.user import User
from db.notifications import (
    get_user_notification_endpoints,
    add_notification,
    set_provider,
    get_total_pages,
    get_notifications
)

class TestNotificationFunctions(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(id=1)  # Создаем пользователя с id=1

    def test_get_user_notification_endpoints(self):
        # Мокаем данные для NotificationAuth
        self.db.query.return_value.filter.return_value.all.return_value = [
            NotificationAuth(method='telegram', id=1, endpoint='https://example.com/telegram'),
            NotificationAuth(method='pwa', id=2, endpoint='https://example.com/pwa'),
        ]

        result = get_user_notification_endpoints(self.db, self.user.id)

        expected = [
            {"provider": "telegram", "provider_id": 1, "endpoint": "https://example.com/telegram"},
            {"provider": "pwa", "provider_id": 2, "endpoint": "https://example.com/pwa"},
        ]
        self.assertEqual(result, expected)

    def test_add_notification(self):
        message = "Test notification"
        url = "https://example.com"
        title = "Test Title"

        # Мокаем поведение базы данных
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        notification = add_notification(self.db, self.user, message, url, title)

        self.db.add.assert_called_once()
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.user_id, self.user.id)
        self.assertEqual(notification.url, url)
        self.assertEqual(notification.title, title)

    def test_set_provider_add(self):
        provider = "telegram"
        endpoint = "https://example.com/telegram"

        # Мокаем поведение базы данных
        self.db.query.return_value.filter_by.return_value.first.return_value = None  # Нет существующей записи

        result = set_provider(self.db, self.user, provider, endpoint)

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.assertTrue(result)

    def test_set_provider_update(self):
        provider = "telegram"
        endpoint = "https://example.com/telegram"

        # Мокаем поведение базы данных
        existing_entry = NotificationAuth(user_id=self.user.id, method=provider, endpoint=endpoint)
        self.db.query.return_value.filter_by.return_value.first.return_value = existing_entry  # Существующая запись

        result = set_provider(self.db, self.user, provider, endpoint)

        self.assertEqual(existing_entry.endpoint, endpoint)  # Проверяем, что endpoint обновился
        self.db.commit.assert_called_once()
        self.assertTrue(result)

    def test_get_total_pages(self):
        # Мокаем количество уведомлений
        self.db.query.return_value.filter.return_value.count.return_value = 100  # 100 уведомлений

        total_pages = get_total_pages(self.db, self.user, on_page=30)

        self.assertEqual(total_pages, 4)  # 100 уведомлений / 30 на странице = 4 страницы

    def test_get_notifications(self):
        # Мокаем уведомления
        self.db.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [
            Notification(message="Test notification 1", user_id=self.user.id),
            Notification(message="Test notification 2", user_id=self.user.id),
        ]

        notifications = get_notifications(self.db, self.user, page=1, on_page=2)

        self.assertEqual(len(notifications), 2)
        self.assertEqual(notifications[0].message, "Test notification 1")
        self.assertEqual(notifications[1].message, "Test notification 2")

if __name__ == '__main__':
    unittest.main()
