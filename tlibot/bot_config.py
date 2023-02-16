from configparser import ConfigParser
from functools import partial

from pyrogram import Client, filters

command = partial(filters.command, prefixes=["!", "/", "."])


class TLI(Client):
    def __init__(self):
        self.name = self.__class__.__name__.lower()
        config = self.load_config()
        super().__init__(
            name=self.name,
            api_id=config["api_id"],
            api_hash=config["api_hash"],
            bot_token=config["bot_token"],
            workers=8,
            plugins=dict(root="tlibot/plugins"),
        )

    async def start(self):
        await super().start()

    async def stop(self, *args):
        await super().stop()

    def load_config(self):
        config = ConfigParser()
        config.read(f"{self.name}.ini")
        return config["tli"]
