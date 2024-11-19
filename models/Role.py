from sqlalchemy import Column, Integer, String, BigInteger
from database.__init__ import Base 
class Role(Base):
    __tablename__ = "role"
    
    
    role_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    
print("Role model created successfully.")