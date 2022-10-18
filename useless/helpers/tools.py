# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

import html

from pyrogram.enums import ChatMemberStatus

from useless import Config, useless


def is_dev(user_id: int) -> bool:
    """return if is dev"""
    return user_id in Config.DEV_USERS


async def check_rights(chat_id: int, user_id: int) -> bool:
    """check admin"""
    user = await useless.get_chat_member(chat_id, user_id)
    if user_id in Config.DEV_USERS:
        return True
    if user.status == ChatMemberStatus.MEMBER:
        return False
    elif user.status == ChatMemberStatus.OWNER or ChatMemberStatus.ADMINISTRATOR:
        return True
    else:
        return False


def mention_html(user_id, name):
    return u'<a href="tg://user?id={}">{}</a>'.format(
        user_id, html.escape(name))
