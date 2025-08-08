# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # 🔄 Vérifie que la connexion est toujours active avant de l'utiliser
    pool_size=10,            # 🔧 Taille du pool de connexions (ajuster selon ta charge)
    max_overflow=20,         # 🔧 Connexions supplémentaires en cas de surcharge
    pool_timeout=30,         # ⏱️ Timeout si trop de connexions sont utilisées
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
