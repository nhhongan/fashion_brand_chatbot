from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database.session import get_db  # Replace with your actual DB session dependency
from models.Product import Product

router = APIRouter(
    prefix="/product",
    tags=["product"]
)



class ProductResponse(BaseModel):
    department: str
    clothing: str
    type_of_clothing: str
    price: str
    color: str

class Query(BaseModel):
    query: str


@router.get("/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    """
    Retrieve all products with specific attributes (department, clothing, type_of_clothing, price, color).
    """
    products = db.query(Product.department, Product.clothing, Product.type_of_clothing, Product.price, Product.color).all()
    
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    
    return products



############# waiting for chatbot
# @router.post("/manual")
# async def manual(item: Item):
#     response = chain.run(
#         department=item.department,
#         clothing=item.clothing,
#         type_of_clothing=item.type_of_clothing,
#         price=item.price,
#         color=item.color
#     )

#     return {response}



# @router.post("/chatbot")
# async def get_answer(query: Query):
#     response = qa.run(
#         query = query.query
#     )

#     return {response}
