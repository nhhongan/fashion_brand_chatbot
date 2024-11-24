from fastapi import FastAPI
from routers import api_routers
from middlewares.cors import apply_cors_middleware
from database.__init__ import engine
from models import Role , User,Payment, Product, Order

#Create database tables
Role.Base.metadata.create_all(bind=engine)
User.Base.metadata.create_all(bind=engine)
Payment.Base.metadata.create_all(bind=engine)
Product.Base.metadata.create_all(bind=engine)
Order.Base.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
    app = FastAPI()
    app = apply_cors_middleware(app)
    app.include_router(api_routers)    
    return app