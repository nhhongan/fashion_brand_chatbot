from sqlalchemy import Column, Integer, String, BigInteger
from database.__init__ import Base 

class Order(Base):
    __tablename__ = "order"
    
    order_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_id = Column(Integer, index=True)
    total_price = Column(BigInteger, index=True)
    payment_id = Column(Integer, index=True)
    
    
    
print("Order model created successfully.")