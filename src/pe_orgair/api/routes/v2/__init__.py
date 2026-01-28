from fastapi import APIRouter

router = APIRouter()

@router.get("/ping", summary="V2 ping")
def ping_v2():
    return {"message": "pong from v2"}