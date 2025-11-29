import fastapi

router = fastapi.APIRouter()


@router.get("/ping")
async def ping():
    return "pong"
