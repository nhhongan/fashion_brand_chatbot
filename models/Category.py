# FILE: Category.py
from sqlalchemy import Column, Integer, String, BigInteger
from database.__init__ import Base 
class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, index=True, primary_key=True)
    name = Column(String, index=True)
    
print("Category model created successfully.")