from fastapi import APIRouter
from .user import router as user_router
from .product import router as product_router 
from .order import router as order_router
from .payment import router as payment_router
from .role import router as role_router

api_routers = APIRouter(prefix="/api/v1")
@api_routers.get('/')
def index():
    return {'message': 'Ecommerce Product Recommendation with ChatGPT'}


api_routers.include_router(user_router)
api_routers.include_router(product_router)
api_routers.include_router(order_router)
api_routers.include_router(payment_router)
api_routers.include_router(role_router)


