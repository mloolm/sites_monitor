import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from models.notification import Notification
from db.sender import send_message
from pwa.pwa_manager import PwaManager
from pywebpush import WebPushException

class TestSendMessage(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.notification = Notification(user_id=1, message="Test message", title="Test Title", url="https://example.com")

    @patch('db.sender.get_user_notification_endpoints')
    @patch('db.sender.send_telegram_notification')
    @patch('pywebpush.webpush')
    @patch('pwa.pwa_manager.PwaManager.get_private_key')
    def test_send_message_telegram_success(self, mock_get_private_key, mock_webpush, mock_send_telegram_notification, mock_get_user_notification_endpoints):

        # Настраиваем моки
        mock_get_user_notification_endpoints.return_value = [
            {"provider": "telegram", "provider_id": 1, "endpoint": '6425916377'}
        ]
        mock_send_telegram_notification.return_value = True

        result = send_message(self.db, self.notification)


        self.assertTrue(result)
        self.notification.sent = True
        self.db.commit.assert_called_once()


    @patch('db.sender.get_user_notification_endpoints')
    @patch('db.sender.webpush')
    @patch('pwa.pwa_manager.PwaManager.get_private_key')
    def test_send_message_pwa_success(self, mock_get_private_key, mock_webpush, mock_get_user_notification_endpoints):
        # Настраиваем моки
        mock_get_user_notification_endpoints.return_value = [
            {"provider": "pwa", "provider_id": 2, "endpoint": '{"endpoint": "https://example.com", "keys": [{"p256dh": "key", "auth": "auth_key"}]}'}
        ]
        mock_get_private_key.return_value = "private_key"
        mock_webpush.return_value = None

        result = send_message(self.db, self.notification)

        self.assertTrue(result)
        self.notification.sent = True
        self.db.commit.assert_called_once()

    @patch('db.sender.get_user_notification_endpoints')
    @patch('db.sender.send_telegram_notification')
    def test_send_message_no_providers(self, mock_send_telegram_notification, mock_get_user_notification_endpoints):
        # Настраиваем моки
        mock_get_user_notification_endpoints.return_value = []

        result = send_message(self.db, self.notification)

        self.assertFalse(result)
        self.db.commit.assert_not_called()

    @patch('db.sender.get_user_notification_endpoints')
    @patch('db.sender.webpush')
    @patch('pwa.pwa_manager.PwaManager.get_private_key')
    def test_send_message_pwa_invalid_endpoint(self, mock_get_private_key, mock_webpush, mock_get_user_notification_endpoints):
        # Настраиваем моки
        mock_get_user_notification_endpoints.return_value = [
            {"provider": "pwa", "provider_id": 2, "endpoint": '{"invalid_key": "value"}'}
        ]
        mock_get_private_key.return_value = "private_key"

        result = send_message(self.db, self.notification)

        self.assertTrue(result)  # Уведомление не отправлено, но функция должна вернуть True
        self.db.commit.assert_not_called()  # Проверяем, что commit не был вызван

    @patch('db.sender.get_user_notification_endpoints')
    @patch('db.sender.webpush')
    @patch('pwa.pwa_manager.PwaManager.get_private_key')
    def test_send_message_pwa_webpush_exception(self, mock_get_private_key, mock_webpush, mock_get_user_notification_endpoints):
        # Настраиваем моки
        mock_get_user_notification_endpoints.return_value = [
            {"provider": "pwa", "provider_id": 2, "endpoint": '{"endpoint": "https://example.com", "keys": {"p256dh": "key", "auth": "auth_key"}}'}
        ]
        mock_get_private_key.return_value = "private_key"
        mock_webpush.side_effect = WebPushException("Push error", response=MagicMock(status_code=404))

        result = send_message(self.db, self.notification)

        self.assertTrue(result)
        self.db.commit.assert_called_once()

