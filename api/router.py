from fastapi import APIRouter
from pyrogram.errors.exceptions import bad_request_400

from api.utils import error_handler
from settings import ADMIN_ID
from tlibot.bot_config import tli_bot

router = APIRouter()


@router.get("/")
async def root():
    return {"root": {"Turkey Learning Initiative"}}


@router.get("/me")
async def hello():
    return {"message": "Hello World"}


@router.get("/say_hello")
async def say_hello(user_id: int = 0, text: str = ""):
    chat_id = user_id or ADMIN_ID

    try:
        message = await tli_bot.send_message(chat_id, text=text or "Hi! I'm FastApi")
    except bad_request_400.PeerIdInvalid as err:
        return await error_handler(400, str(err))
    except Exception as err:
        return await error_handler(500, str(err))

    return {
        "status": 200,
        "date": message.date,
        "chat_type": message.chat.type.value,
        "text": message.text,
    }
