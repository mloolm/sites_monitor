# main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from db.session import get_db, Base, engine
from db.crud import authenticate_user, create_access_token
from sqlalchemy.orm import Session
from fastapi import Request
from models.notification_auth import NotificationAuth
from services.notification_providers.telegram import handle_telegram_webhook
from pwa.pwa_manager import PwaManager
from contextlib import asynccontextmanager

# Creates the tables in the database when the application starts.
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    PwaManager.gen_keys()
    yield


# Creates an instance of FastAPI.
app = FastAPI(
    title="Site Monitoring API",
    description="API for website and SSL certificate monitoring.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routes import router as api_router
app.include_router(api_router, prefix="/api")

# Adds a basic route to check if the API is working.
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
        webhook_hash: str,
        request: Request,
        db: Session = Depends(get_db)
):
    """
    Route for receiving webhooks from Telegram.
    Checks if the provided hash matches the expected value.
    """
    # expected hash
    expected_hash = NotificationAuth.get_telegram_webhook_url_hash()

    if not expected_hash:
        raise HTTPException(status_code=404, detail="Page not found")

    # Checks if the provided hash matches the expected one.
    if webhook_hash != expected_hash:
        raise HTTPException(status_code=404, detail="Page not found")

    # Gets the data from the request.
    data = await request.json()

    # Passes the data to the webhook handling method.
    response = handle_telegram_webhook(db, data)

    return response


