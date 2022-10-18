# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

from pyrogram import filters
from pyrogram.types import Message

from useless import useless, trg
from useless.helpers import is_dev, Groups


@useless.on_message(filters.command(["stats", "status"], trg))
async def status_(_, m: Message):
    user_id = m.from_user.id
    if not is_dev(user_id):
        return
    msg = await m.reply("`Processing ...`")
    await msg.edit(f"──❑ 「 <b>Bot Stats</b> 」 ❑──\n\n# Groups: <code>{await Groups.count()}</code>")


@useless.on_message(filters.new_chat_members)
async def thanks_for(c: useless, m: Message):
    gid = m.chat.id
    if c.me.id in [x.id for x in m.new_chat_members]:
        if await Groups.find_gp(gid):
            return
        else:
            await Groups.add_gp(m)


@useless.on_message(filters.left_chat_member)
async def left_chat_(c: useless, m: Message):
    gid = m.chat.id
    if c.me.id == m.left_chat_member.id:
        if await Groups.find_gp(gid):
            await Groups.rm_gp(gid)
        else:
            return
