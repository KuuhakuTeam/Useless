# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

import random
import requests

from gpytranslate import Translator
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import ChatIdInvalid, ChatWriteForbidden, ChannelInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


from useless import useless, trg
from useless.helpers import db, check_rights, Groups


DB = db("GROUPS")
API = "https://uselessfacts.jsph.pl/random.json?language=en"

scheduler = AsyncIOScheduler()


@useless.on_message(filters.command(["start"], trg))
async def starting(_, message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Repository", url=f"https://github.com/KuuhakuTeam/Useless/",
                ),
                InlineKeyboardButton(
                    text="Add to a group", url=f"https://t.me/{useless.me.username}?startgroup=new",
                ),
            ],
        ]
    )
    if message.chat.type == ChatType.PRIVATE:
        await useless.send_photo(message.chat.id, "https://telegra.ph/file/2ce17b14b27631a05a113.png", caption=random.choice(RANDOM), reply_markup=keyboard)
    else:
        msg = "<b>/addchat - to add chat to bot info list\n/lang - to set the information language\n/stop - to stop receiving messages from me here.</b>"
        await message.reply(msg)


@useless.on_message(filters.command("addchat", trg))
async def add_to_list(_, message):
    chat_id = message.chat.id
    if not message.chat.type == ChatType.SUPERGROUP:
        return
    if not await check_rights(message.chat.id, message.from_user.id):
        return await message.reply("<i>You need to be admin to do this.</i>")
    if await Groups.find_gp(chat_id):
        await message.reply("<i>The chat is already on the useless list.</i>")
    else:
        await Groups.add_gp(message)
        await message.reply("<i>Chat has been added to useless list</i>")


@useless.on_message(filters.command("lang", trg))
async def set_lang_(_, message):
    chat_id = message.chat.id
    if not message.chat.type == ChatType.SUPERGROUP:
        return
    if not await check_rights(message.chat.id, message.from_user.id):
        return await message.reply("<i>You need to be admin to do this.</i>")
    if not await Groups.find_gp(chat_id):
        await message.reply("<i>This chat is not on the useless list, use /addchat to add.</i>")
    else:
        buttons_ = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🇧🇷 Português", callback_data=f"_lang|pt"),
                    InlineKeyboardButton(
                        "🇺🇸 English", callback_data=f"_lang|en")
                ],
            ]
        )
        await message.reply("<i>Select language in which you want to receive information</i>", reply_markup=buttons_)


@useless.on_callback_query(filters.regex(pattern=r"^_lang\|(.*)"))
async def set_language(_, cb: CallbackQuery):
    data, lang = cb.data.split("|")
    gid = cb.message.chat.id
    if cb.message.chat.type == ChatType.SUPERGROUP:
        if not await check_rights(gid, cb.from_user.id):
            return await cb.answer("You need to be admin to do this", show_alert=True)
    if lang == "pt":
        await Groups.add_lang(gid, "pt")
    else:
        await Groups.add_lang(gid, "en")
    await cb.edit_message_text(f"Information will be sent in {lang}")


@useless.on_message(filters.command("stop", trg))
async def stop_infos(_, message):
    chat_id = message.chat.id
    if not message.chat.type == ChatType.SUPERGROUP:
        return
    if not await check_rights(message.chat.id, message.from_user.id):
        return await message.reply("<i>You need to be admin to do this.</i>")
    if await Groups.find_gp(chat_id):
        await Groups.rm_gp(chat_id)
        await message.reply("<i>Okay, I won't send messages here anymore.</i>")
    else:
        await message.reply("<i>This chat is not on the useless list.</i>")


async def info():
    glist = DB.find()
    async for chats in glist:
        if chats == None:
            return
        else:
            gid = chats["_id"]
            data = requests.get(API).json()
            msg = data["text"]
            lang = await Groups.find_lang(gid)
            if lang == "pt":
                tr = Translator()
                tr_ = await tr.translate(msg, targetlang="pt")
                msg = tr_.text
            try:
                await useless.send_message(chat_id=gid, text=msg)
            except (ChatIdInvalid, ChannelInvalid):
                await Groups.rm_gp(gid)
                pass
            except ChatWriteForbidden:
                pass
            except Exception as e:
                await useless.send_log(e, disable_notification=False, disable_web_page_preview=True)
                pass


RANDOM = [
    "No number from 1 to 999 includes the letter \"a\" in its word form.",
    "The opposite sides of a die will always add up to seven.",
    "You are 13.8 percent more likely to die on your birthday.",
    "Playing dance music can help ward off mosquitoes.",
    "If you open your eyes in a pitch-black room, the color you'll see is called \"eigengrau\".",
    "Cats can't taste sweet things because of a genetic defect.",
    "Pogonophobia is the fear of beards."
]
