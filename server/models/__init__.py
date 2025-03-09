# models/__init__.py
from .site import Site
from .user import User
from .monitor import Monitor
# Экспортируем все модели
__all__ = ["Site","User", "Monitor"]