from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.posts import router as posts_router
from app.api.users import router as users_router

app = FastAPI(title="JustTalk API")

# CORS — dev: Vite на localhost / 127.0.0.1 (явно + regex на любой порт).
# allow_private_network: иначе Chrome может ронять preflight на localhost API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_origin_regex=r"http://(127\.0\.0\.1|localhost):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_private_network=True,
)

# Роутеры
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(users_router)

# Базовые ручки
@app.get("/")
def root():
    return {"message": "Welcome to JustTalk API"}

@app.get("/health")
def health():
    return {"status": "ok"}