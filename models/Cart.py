# FILE: Cart.py
from sqlalchemy import Column, Integer, ForeignKey
from database.base import Base  # Assuming Base is defined in a module named base

class Cart(Base):
    __tablename__ = "cart"
    order_id = Column(Integer, ForeignKey('order.order_id'), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), primary_key=True, index=True)
    quantity = Column(Integer, index=True)
    
    
print("Cart model created successfully.")