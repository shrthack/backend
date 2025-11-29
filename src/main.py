import fastapi
import uvicorn

from internal.config import settings
from internal.handlers import other
from internal.handlers import client

app = fastapi.FastAPI()
app.include_router(other.router, tags=["Check"])
app.include_router(client.router, tags=["Client"])


def main():
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)


if __name__ == "__main__":
    main()
