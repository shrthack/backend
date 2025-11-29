import fastapi
import uvicorn

from internal.config import settings
from internal.handlers import other
from internal.handlers import client
from internal.handlers import event

app = fastapi.FastAPI()
app.include_router(other.router, tags=["Check"])
app.include_router(client.router, tags=["Client"])
app.include_router(event.router, tags=["Event"])


def main():
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)


if __name__ == "__main__":
    main()
