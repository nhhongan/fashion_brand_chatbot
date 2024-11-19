from database import SessionLocal
from sqlalchemy.orm import Session
from . import engine

session = Session(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()