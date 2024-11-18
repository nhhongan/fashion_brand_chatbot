from fastapi import FastAPI
from routers import api_routers
from middlewares.cors import apply_cors_middleware
from database import Base, engine  
from database.__init__ import init_db



def create_app() -> FastAPI:
    app = FastAPI()
    app = apply_cors_middleware(app)
    app.include_router(api_routers)
    
    @app.on_event("startup")
    async def startup():
        init_db()

    
    
    return app