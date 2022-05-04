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
from useless.helpers import get_collection, is_dev


GROUPS = get_collection("GROUPS")


@useless.on_message(filters.command(["stats", "status"], trg))
async def status_(_, m: Message):
    user_id = m.from_user.id
    if not is_dev(user_id):
        return
    msg = await m.reply("`Processing ...`")
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    glist = await GROUPS.estimated_document_count()
    ulist = await USERS.estimated_document_count()
    await msg.edit(f"""
╭─❑ 「 **Bot Stats** 」 ❑──
│- __Users:__ `{ulist}`
│- __Groups:__ `{glist}`
╰❑

╭─❑ 「 **Hardware Usage** 」 ❑──
│- __CPU Usage:__ `{cpu_usage}%`
│- __RAM Usage:__ `{ram_usage}%`
╰❑
""")


@useless.on_message(filters.new_chat_members)
async def thanks_for(c: useless, m: Message):
    user = (
        f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>")
    gp_title = m.chat.title
    gp_id = m.chat.id
    text_add = f"#Useless #New_Group\n\n**Group**: __{gp_title}__\n**ID:** __{gp_id}__\n**User:** __{user}__"
    if m.chat.username:
        text_add += f"**\nUsername:** @{m.chat.username}"
    if c.me.id in [x.id for x in m.new_chat_members]:
        try:
            await c.send_message(
                chat_id=m.chat.id,
                text=(f"{random.choice(FRASES)}\n\nreport bugs em -> @fnixsup__"),
                disable_notification=True,
            )
        except ChatWriteForbidden:
            print("\n[ ERROR ] Bot cannot send messages\n")
        found = await GROUPS.find_one({"_id": gp_id})
        if not found:
            await asyncio.gather(
                GROUPS.insert_one({"_id": gp_id, "title": gp_title}),
                c.send_log(
                    text_add,
                    disable_notification=False,
                    disable_web_page_preview=True,
                )
            )


@useless.on_message(filters.left_chat_member)
async def left_chat_(c: useless, m: Message):
    gp_title = m.chat.title
    gp_id = m.chat.id
    text_add = f"#Useless #Left_Group\n\n**Group**: __{gp_title}__\n**ID:** __{gp_id}__"
    if c.me.id == m.left_chat_member.id:
        found = await GROUPS.find_one({"_id": gp_id})
        if found:
            await asyncio.gather(
                GROUPS.delete_one({"_id": gp_id, "title": gp_title}),
                c.send_log(
                    text_add,
                    disable_notification=False,
                    disable_web_page_preview=True,
                )
            )
        else:
            return


FRASES = [
  "Toda cagada requer uma mijada, mas nem toda mijada requer uma cagada ~ `Leonardo Davinci`.",
  "Nem todo humano é gay, e nem todo gay é humano ~ `Nelson Mandela`",
  "Não tem problema peidar enquanto mija afinal, não existe chuva sem trovão ~ `Martin Luther King`",
  "Nem todo corinthiano é ladrão, mas rodo ladrão é corinthiano ~ `Freud`"
  ]
