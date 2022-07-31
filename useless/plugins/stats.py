# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

import asyncio
import psutil
import random

from pyrogram.errors import ChatWriteForbidden
from pyrogram import filters
from pyrogram.types import Message

from useless import useless, trg
from useless.helpers import db, is_dev, rm_gp, add_gp, find_gp


GROUPS = db("GROUPS")


@useless.on_message(filters.command(["stats", "status"], trg))
async def status_(_, m: Message):
    user_id = m.from_user.id
    if not is_dev(user_id):
        return
    msg = await m.reply("`Processing ...`")
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    glist = await GROUPS.estimated_document_count()
    await msg.edit(f"""
╭─❑ 「 **Bot Stats** 」 ❑──
│- __Groups:__ `{glist}`
╰❑

╭─❑ 「 **Hardware Usage** 」 ❑──
│- __CPU Usage:__ `{cpu_usage}%`
│- __RAM Usage:__ `{ram_usage}%`
╰❑
""")


@useless.on_message(filters.new_chat_members)
async def thanks_for(c: useless, m: Message):
    gid = m.chat.id
    if c.me.id in [x.id for x in m.new_chat_members]:
        if await find_gp(gid):
            return
        else:
            await add_gp(m)


@useless.on_message(filters.left_chat_member)
async def left_chat_(c: useless, m: Message):
    gid = m.chat.id
    if c.me.id == m.left_chat_member.id:
        if await find_gp(gid):
            await rm_gp(gid)
        else:
            return
