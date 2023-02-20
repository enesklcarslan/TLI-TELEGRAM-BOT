from configparser import ConfigParser
from functools import partial

from pyrogram import Client, filters

from settings import API_HASH, API_ID, BOT_TOKEN

command = partial(filters.command, prefixes=["!", "/", "."])


class TLI(Client):
    def __init__(self):
        self.name = self.__class__.__name__.lower()
        super().__init__(
            name=self.name,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=8,
            plugins=dict(root="tlibot/plugins"),
        )

    async def start(self):
        await super().start()

    async def stop(self, *args):
        await super().stop()
