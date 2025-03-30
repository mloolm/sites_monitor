import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from db.monitor import get_sites_health, get_site_data
from  models.monitor import Monitor
from models.monitor_by_days import MonitorByDay

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_get_sites_health(mock_db):
    # Создаем моки для сайтов
    sites = [MagicMock(id=1), MagicMock(id=2)]

    # Настраиваем поведение мока для первого SQL-запроса (monitor)
    mock_db.execute.return_value.fetchall.side_effect = [
        [
            MagicMock(site_id=1, total_checks=10, successful_checks=8),
            MagicMock(site_id=2, total_checks=5, successful_checks=5)
        ],
        # Настраиваем поведение для второго SQL-запроса (ssl_monitor)
        [
            MagicMock(site_id=1, valid_to=datetime.utcnow() + timedelta(days=30)),
            MagicMock(site_id=2, valid_to=datetime.utcnow() + timedelta(days=30))
        ]
    ]

    health_data = get_sites_health(mock_db, sites)

    assert health_data[1]['up'] == 80  # 8 успешных из 10
    assert health_data[2]['up'] == 100  # 5 успешных из 5
    assert health_data[1]['ssl'] is not None  # Должен быть валидный SSL
    assert health_data[2]['ssl'] is not None  # Должен быть валидный SSL


def test_get_site_data_week(mock_db):
    site_id = 1
    mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
        MagicMock(check_dt=datetime.utcnow() - timedelta(days=1), is_ok=True, code=200, response_time_ms=100),
        MagicMock(check_dt=datetime.utcnow() - timedelta(days=2), is_ok=False, code=500, response_time_ms=200)
    ]


    result = get_site_data(mock_db, site_id, period='week')


    assert len(result) == 2
    assert result[0]['check_dt'] is not None
    assert result[0]['is_ok'] is True
    assert result[1]['is_ok'] is False

def test_get_site_data_month(mock_db):
    site_id = 1
    mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
        MagicMock(check_dt=datetime.utcnow() - timedelta(days=10), uptime=99.9),
        MagicMock(check_dt=datetime.utcnow() - timedelta(days=20), uptime=98.5)
    ]


    result = get_site_data(mock_db, site_id, period='month')


    assert len(result) == 2
    assert result[0]['check_dt'] is not None
    assert result[0]['uptime'] == 99.9

def test_get_site_data_invalid_period(mock_db):
    site_id = 1
    with pytest.raises(ValueError, match="Bad period invalid"):
        get_site_data(mock_db, site_id, period='invalid')
