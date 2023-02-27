from settings import ADMIN_ID
from tlibot.bot_config import tli_bot


async def error_handler(status: int, message: str):
    if ADMIN_ID:
        await tli_bot.send_message(ADMIN_ID, message)

    return {"status": status, "message": message}
