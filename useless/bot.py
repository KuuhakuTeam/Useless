# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

from pyrogram import Client
from .config import Config

import time
import os

from dotenv import load_dotenv

if os.path.isfile("config.env"):
    load_dotenv("config.env")

START_TIME = time.time()

class UselessBot(Client):
    def __init__(self):
        kwargs = {
            'name': "useless",
            'api_id': Config.API_ID,
            'api_hash': Config.API_HASH,
            'bot_token': Config.BOT_TOKEN,
            'in_memory': True,
            'plugins': dict(root="useless.plugins")
        }
        super().__init__(**kwargs)

    async def start(self):
        await super().start()
        self.me = await self.get_me()
        await self.send_message(chat_id=Config.GP_LOGS, text="bot started")
        print("bot running...")

    async def stop(self):
        await super().stop()
        print("shutdown...")

    async def send_log(self, text: str, *args, **kwargs):
        await self.send_message(
            chat_id=Config.GP_LOGS,
            text=text,
            *args,
            **kwargs,
        )


useless = UselessBot()
