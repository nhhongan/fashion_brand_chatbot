from fastapi import APIRouter

router = APIRouter(
    prefix="/payment",
    tags=["payment"]
)