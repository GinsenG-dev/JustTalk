from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.users import router as users_router

app = FastAPI(title="JustTalk API")

# CORS — чтобы фронт (http://localhost:5173) мог ходить на бэк (http://localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(auth_router)
app.include_router(users_router)

# Базовые ручки
@app.get("/")
def root():
    return {"message": "Welcome to JustTalk API"}

@app.get("/health")
def health():
    return {"status": "ok"}