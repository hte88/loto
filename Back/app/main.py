# app/main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.api.routes import router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router, prefix="/api")


app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # l'URL de ton front
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
