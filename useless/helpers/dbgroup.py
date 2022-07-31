# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

from useless import useless
from .core import db

GROUPS = db("GROUPS")


async def find_gp(gid: int):
    if await GROUPS.find_one({"_id": gid}):
        return True


async def add_gp(m):
    user = f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>"
    user_start = f"#Usekess #New_Group\n\n<b>Group</b>: {m.chat.title}\n<b>ID:</b> {m.chat.id}\n<b>User:</b> {user}"
    await useless.send_log(
        user_start, disable_notification=False, disable_web_page_preview=True
        )
    await GROUPS.insert_one({"_id": m.chat.id})


async def rm_gp(gid: int):
    await GROUPS.delete_one({"_id": gid})


async def find_lang(gid: int):
    find = await GROUPS.find_one({"_id": gid})
    try:
        return find["lang"]
    except (KeyError, TypeError):
        return "pt"


async def add_lang(gid: int, lang: str):
    await GROUPS.update_one(
            {"_id": gid},
            {"$set": {"lang": lang}},
        upsert=True
    )
