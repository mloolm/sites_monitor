import pytest
from unittest.mock import Mock, create_autospec
from sqlalchemy.orm import Session
from models.user import User
from models.site import Site
from models.notification_auth import NotificationAuth
from datetime import datetime, timedelta
from jose import jwt
from core.config import settings
import db.crud as mut


@pytest.fixture
def mock_db():
    return create_autospec(Session, instance=True)


@pytest.fixture
def sample_user():
    user = User(login="testuser")
    user.set_password("testpass")
    return user


class TestUserFunctions:
    def test_create_user(self, mock_db, sample_user):
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        result = mut.create_user(mock_db, "testuser", "testpass")

        assert isinstance(result, User)
        assert result.login == "testuser"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_get_user_by_login_existing(self, mock_db, sample_user):
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user

        result = mut.get_user_by_login(mock_db, "testuser")

        assert result == sample_user

    def test_get_user_by_login_nonexistent(self, mock_db):
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = mut.get_user_by_login(mock_db, "nonexistent")

        assert result is None

    def test_authenticate_user_success(self, mock_db, sample_user):
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user

        result = mut.authenticate_user(mock_db, "testuser", "testpass")

        assert result == sample_user

    def test_authenticate_user_wrong_password(self, mock_db, sample_user):
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user

        result = mut.authenticate_user(mock_db, "testuser", "wrongpass")

        assert result is None

    def test_authenticate_user_nonexistent(self, mock_db):
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = mut.authenticate_user(mock_db, "nonexistent", "anypass")

        assert result is None


class TestTokenFunctions:
    def test_create_access_token(self):
        test_data = {"sub": "testuser"}
        result = mut.create_access_token(test_data)

        assert isinstance(result, str)
        decoded = jwt.decode(result, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert decoded["sub"] == "testuser"
        assert "exp" in decoded


class TestSiteFunctions:
    def test_create_site(self, mock_db, sample_user):
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = Site(id=1, url="http://test.com", user_id=sample_user.id)

        result = mut.create_site(mock_db, sample_user, "http://test.com")

        assert isinstance(result, Site)
        assert result.url == "http://test.com"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_get_site_exists(self, mock_db, sample_user):
        test_site = Site(id=1, url="http://test.com", user_id=sample_user.id)
        mock_db.query.return_value.filter.return_value.first.return_value = test_site

        result = mut.get_site(mock_db, sample_user, 1)

        assert result == test_site

    def test_get_site_not_exists(self, mock_db, sample_user):
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = mut.get_site(mock_db, sample_user, 999)

        assert result is None

    def test_get_sites(self, mock_db, sample_user):
        # Создаем mock для query объекта
        mock_query = Mock()
        mock_db.query.return_value.filter.return_value = mock_query

        # Настраиваем mock для возврата тестовых данных
        test_sites = [
            Site(id=1, url="http://test1.com", user_id=sample_user.id),
            Site(id=2, url="http://test2.com", user_id=sample_user.id)
        ]
        mock_query.all.return_value = test_sites

        # Вызываем тестируемую функцию
        query_result = mut.get_sites(mock_db, sample_user)

        # Получаем фактические результаты (имитируем вызов all())
        actual_sites = query_result.all()

        # Проверяем что результаты соответствуют ожидаемым
        assert actual_sites == test_sites

    def test_delete_site_exists(self, mock_db, sample_user):
        test_site = Site(id=1, url="http://test.com", user_id=sample_user.id)
        mock_db.query.return_value.filter.return_value.first.return_value = test_site

        result = mut.delete_site(mock_db, sample_user, 1)

        assert result is True
        mock_db.delete.assert_called_once_with(test_site)
        mock_db.commit.assert_called_once()

    def test_delete_site_not_exists(self, mock_db, sample_user):
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = mut.delete_site(mock_db, sample_user, 999)

        assert result is False
        mock_db.delete.assert_not_called()
        mock_db.commit.assert_not_called()


class TestNotificationFunctions:
    def test_get_user_noty_providers(self, mock_db, sample_user):
        test_providers = [
            NotificationAuth(id=1, method="email", user_id=sample_user.id, endpoint='xxx'),
            NotificationAuth(id=2, method="telegram", user_id=sample_user.id, endpoint='yyy')
        ]
        mock_db.query.return_value.filter.return_value.all.return_value = test_providers

        result = mut.get_user_noty_providers(mock_db, sample_user)

        assert result == test_providers