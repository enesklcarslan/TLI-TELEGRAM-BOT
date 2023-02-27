from fastapi import FastAPI

import settings
from api.router import router
from tlibot.bot_config import tli_bot


async def startup():
    await tli_bot.start()


async def shutdown():
    await tli_bot.stop()


def get_application() -> FastAPI:
    fast_app = FastAPI()

    fast_app.add_event_handler("startup", startup)
    fast_app.add_event_handler("shutdown", shutdown)
    fast_app.include_router(router)

    return fast_app


app = get_application()


def main():
    import uvicorn

    uvicorn.run("api.main:app", reload=settings.DEBUG)
