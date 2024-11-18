from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from .base import Base
from decouple import config
from models import Cart, Order, Product , Payment, Role , User , Category
# Import all the models in the database

URL_DATABASE = "postgresql+asyncpg://admin:123admin@db:5432/chatbotAI"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create all tables in the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)