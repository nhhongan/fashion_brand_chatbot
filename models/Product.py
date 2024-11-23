
from sqlalchemy import Column, Integer, String, BigInteger,ForeignKey
from database.__init__ import Base 
class Product(Base):
    __tablename__ = "product"
    
    product_id = Column(Integer,primary_key=True, index=True,autoincrement=True)
    name = Column(String, index=True)
    department = Column(String, index=True)
    clothing = Column(String, index=True)
    type_of_clothing = Column(String, index=True)
    price = Column(BigInteger, index=True)
    color = Column(String, index=True)
    


print("Product model created successfully.")