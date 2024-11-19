from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from decouple import config
from sqlalchemy.ext.declarative import declarative_base

# Import all the models in the database

URL_DATABASE = "postgresql://admin:123admin@db:5432/chatbotAI"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()