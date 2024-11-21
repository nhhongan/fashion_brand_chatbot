
from sqlalchemy import Column, Integer, String, BigInteger,ForeignKey
from database.__init__ import Base 
class Product(Base):
    __tablename__ = "product"
    
    product_id = Column(Integer,primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('category.category_id') ,index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(BigInteger, index=True)
    image = Column(String, index=True)
    color = Column(String, index=True)
    


print("Product model created successfully.")