import fastapi
import uvicorn

from internal.config import settings
from internal.handlers import other
from internal.handlers import client
from internal.handlers.merch import router as merch_router

app = fastapi.FastAPI()
app.include_router(other.router, tags=["Check"])
app.include_router(client.router, tags=["Client"])
app.include_router(merch_router, tags=["Merch"])


def main():
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)


if __name__ == "__main__":
    main()
