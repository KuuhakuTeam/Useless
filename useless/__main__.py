# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

from .bot import useless
from pyrogram import idle
import asyncio
from .helpers.db import _close_db

async def main():
    await useless.start()
    await idle()
    await useless.stop()
    _close_db()

if __name__ == "__main__" :
    asyncio.get_event_loop().run_until_complete(main())
