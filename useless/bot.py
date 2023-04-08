# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

import os
import time

from dotenv import load_dotenv
from pyrogram import Client
from .config import Config

if os.path.isfile("config.env"):
    load_dotenv("config.env")

START_TIME = time.time()
VERSION = "v1.0.2"


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
        await self.send_message(chat_id=Config.GP_LOGS, text=f"bot running ...\n- {VERSION}")
        print(f"bot running ...\n- {VERSION}")

    async def stop(self):
        await super().stop()
        print("shutdown ...")

    async def send_log(self, text: str, *args, **kwargs):
        await self.send_message(
            chat_id=Config.GP_LOGS,
            text=text,
            *args,
            **kwargs,
        )

    async def leave(self, gid: int):
        await self.leave_chat(chat_id=gid)


useless = UselessBot()
