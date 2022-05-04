# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

import os
import sys
import json
import random
import asyncio
import requests

from gpytranslate import Translator

from pyrogram.errors import ChatIdInvalid, ChatWriteForbidden
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import filters

from useless import useless, Config, trg
from useless.helpers import get_collection, check_rights, is_dev


DB = get_collection("GROUPS")
API = "https://uselessfacts.jsph.pl/random.json?language=en"


@useless.on_message(filters.command(["start", "help", "about"], trg))
async def spam(useless, message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Repositorio", url=f"https://github.com/KuuhakuTeam/Useless/",
                ),
                InlineKeyboardButton(
                    text="Add a um grupo", url=f"https://t.me/{useless.me.username}?startgroup=new",
                ),
            ],
        ]
    )
    if message.chat.type == ChatType.PRIVATE:
        await useless.send_photo(message.chat.id, "https://telegra.ph/file/c8fbbcb6a72c7bdf98ade.jpg", caption=random.choice(RANDOM), reply_markup=keyboard)
    else:
        msg = "/addchat - para adicionar o chat a lista de informações do bot \n/stop - para parar de receber mensagens minha aqui."
        await message.reply(msg)

@useless.on_message(filters.command("loop"))
async def spam(useless, message):
    if not message.from_user.id == 838926101:
        return
    await useless.send_message(message.chat.id, "loop started")
    while True:
        await infos_()
        await asyncio.sleep(10)


@useless.on_message(filters.command("cleardb"))
async def spam(useless, message):
    if not message.from_user.id == 838926101:
        return
    await DB.drop()


@useless.on_message(filters.command("addchat"))
async def set_time(useless, message):
    chat_id = message.chat.id
    if not message.chat.type == ChatType.SUPERGROUP:
        return
    if not await check_rights(message.chat.id, message.from_user.id):
        return await message.reply("__Você precisa ser adm pra fazer isso.__")
    found = await DB.find_one({"_id": chat_id})
    if found:
        await message.reply("__O chat ja esta na lista inútil.__")
    else:
        await DB.insert_one({"_id": chat_id})
        await message.reply("__Chat adicionado na lista inútil.__")


@useless.on_message(filters.command("stop"))
async def set_lang(useless, message):
    chat_id = message.chat.id
    if not message.chat.type == ChatType.SUPERGROUP:
        return
    if not await check_rights(message.chat.id, message.from_user.id):
        return await message.reply("__Você precisa ser adm pra fazer isso.__")
    found = await DB.find_one({"_id": chat_id})
    if found:
        await DB.delete_one({"_id": chat_id})
        await message.reply("__Ok, não enviarei mais mensagens aqui.__")
    else:
        await message.reply("__Este chat não esta na lista inútil.__")


@useless.on_message(filters.command("reset"))
async def spam(useless, message):
    if not message.from_user.id == 838926101:
        return
    await message.reply("kek")
    os.execv(sys.executable, [sys.executable, "-m", "useless"])


async def infos_():
    glist = DB.find()
    async for chats in glist:
        if chats == None:
            return
        else:
            r = requests.get(API).json()
            msg = r["text"]
            tr = Translator()
            tr_ = await tr.translate(msg, targetlang="pt")
            try:    
                await useless.send_message(chats["_id"], tr_.text)
            except ChatIdInvalid:
                pass
            except ChatWriteForbidden:
                pass


RANDOM = [
  "Ketchup foi vendido como remédio nos anos de 1830.",
  "Os pinguins têm glândulas abaixo dos olhos para extrair o excesso de sal. Elas são poderosas o bastante para permitir que eles tenham a água do mar como principal fonte de água",
  "Cavalos não conseguem vomitar.",
  "A baleia assassina é a predadora natural do alce. Baleias assassinas atacam os alces enquanto eles nadam de uma ilha a outra na busca por comida",
  "No Japão feudal, os lordes propositalmente construíam casas com um pavimento que chiava, como medida defensiva contra ninjas.",
  "Um segundo é chamado de um segundo porque é a segunda divisão da hora por 60, sendo a primeira divisão o minuto."
  ]