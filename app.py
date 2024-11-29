from fastapi import FastAPI
from routers import api_routers
from middlewares.cors import apply_cors_middleware
from database.__init__ import engine
from database import setup



def create_app() -> FastAPI:
    app = FastAPI()
    app = apply_cors_middleware(app)
    app.include_router(api_routers)   
    return app