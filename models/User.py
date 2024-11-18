from sqlalchemy import Column, Integer, String, BigInteger
from database.base import Base 

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    address = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(Integer, index=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    role_id = Column(Integer, index=True)
    
    
print("User model created successfully.")
