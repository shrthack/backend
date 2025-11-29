import fastapi
import uvicorn

from internal.config import settings
from internal.handlers import other
from internal.handlers import client
from internal.handlers import analytics

from internal.handlers.merch import router as merch_router
from internal.handlers import event
from internal.handlers import stand
from internal.handlers import points

app = fastapi.FastAPI()
app.include_router(other.router, tags=["Check"])
app.include_router(client.router, tags=["Client"])
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(merch_router, tags=["Merch"])
app.include_router(event.router, tags=["Event"])
app.include_router(stand.router, tags=["Stand"])
app.include_router(points.router, tags=["Points"])


def main():
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)


if __name__ == "__main__":
    main()
