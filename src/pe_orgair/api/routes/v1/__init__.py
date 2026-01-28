from fastapi import APIRouter

router = APIRouter()

@router.get("/ping", summary="V1 ping")
def ping_v1():
    return {"message": "pong from v1"}
from pe_orgair.schemas.greet import GreetUserRequest

@router.post("/greet", summary="Greet a user")
def greet_user(payload: GreetUserRequest):
    return f"Hello {payload.name}, age {payload.age}!"
from pe_orgair.api.routes.v1.items import router as items_router
router.include_router(items_router)
from pe_orgair.api.routes.v1.sector_config import router as sector_router
app.include_router(sector_router)