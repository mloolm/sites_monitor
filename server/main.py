# main.py
from fastapi import FastAPI
from core.config import settings  # Импортируем настройки, если нужно

# Создаём экземпляр FastAPI
app = FastAPI(
    title="Site Monitoring API",
    description="API для мониторинга сайтов и SSL-сертификатов",
    version="1.0.0",
)

# Подключаем маршруты
from api.routes import router as api_router
app.include_router(api_router, prefix="/api")

# Добавляем базовый маршрут для проверки работоспособности
@app.get("/")
def read_root():
    return {"message": "Welcome to the Site Monitoring API"}