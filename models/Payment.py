from sqlalchemy import Column, Integer, String, BigInteger
from database.base import Base 

class Payment(Base):
    __tablename__ = "payment"
    
    payment_id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    
    
    
print("Payment model created successfully.")