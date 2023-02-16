import asyncio

from pyrogram import Client
from pyrogram.types import Message

from tlibot.bot_config import TLI, command


@TLI.on_message(command("start"))
async def say_hello(_: Client, message: Message) -> None:
    msg = await message.reply_text(text="`Hello..`", quote=True)
    await asyncio.sleep(1)
    await msg.edit_text(text="`Hello I'm Ready to Use`")
