# main.py
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from api.auth import oauth2_scheme
from pydantic import BaseModel
from db.session import get_db, Base, engine
from db.crud import authenticate_user, create_access_token
from sqlalchemy.orm import Session
from fastapi import Request
from models.notification_auth import NotificationAuth
from services.notification_providers.telegram import handle_telegram_webhook
from pwa.pwa_manager import PwaManager
from contextlib import asynccontextmanager

# Создаем таблицы в базе данных при запуске приложения
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    PwaManager.gen_keys()
    yield


# Создаём экземпляр FastAPI
app = FastAPI(
    title="Site Monitoring API",
    description="API для мониторинга сайтов и SSL-сертификатов",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем маршруты
from api.routes import router as api_router
app.include_router(api_router, prefix="/api")

# Добавляем базовый маршрут для проверки работоспособности
@app.get("/")
def read_root():
    return {"message": "Welcome to the Site Monitoring API"}

class TokenRequest(BaseModel):
    username: str
    password: str

@app.post("/api/token")
async def login(
        request: TokenRequest,
        db: Session = Depends(get_db)
):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.login}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/telegram/webhook/{webhook_hash}")
async def telegram_webhook(
        webhook_hash: str,  # Параметр пути для хэша
        request: Request,
        db: Session = Depends(get_db)
):
    """
    Роут для приема вебхуков от Telegram.
    Проверяет, соответствует ли переданный hash ожидаемому значению.
    """
    # Получаем ожидаемый hash
    expected_hash = NotificationAuth.get_telegram_webhook_url_hash()

    if not expected_hash:
        raise HTTPException(status_code=404, detail="Page not found")

    # Проверяем, совпадает ли переданный hash с ожидаемым
    if webhook_hash != expected_hash:
        raise HTTPException(status_code=404, detail="Page not found")

    # Получаем данные из запроса
    data = await request.json()

    # Передаем данные в метод обработки вебхука
    response = handle_telegram_webhook(db, data)

    return response


