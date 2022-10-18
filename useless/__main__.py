# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

from .bot import useless
from pyrogram import idle
import asyncio
from .helpers.core import _close_db
from useless.plugins.useless import info

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def main():
    await useless.start()
    scheduler.add_job(info, "interval", hours=3, id='useless')
    scheduler.start()
    await idle()
    await useless.stop()
    _close_db()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
