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


@useless.on_message(filters.command("delchat", trg))
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
    "Flamingos can only eat with their heads upside down.\n\nThese tall pink characters use their tongue as a sieve to catch food by flipping their heads about. The flamingo’s tongue helps pump the food-filled water in and out of their mouths about three times a second. This technique is called filter feeding! ",
    "A blob of toothpaste is called a nurdle.\n\nNobody is quite sure where the word 'nurdle' originated. A fact as useless as the word.",
    "The moon has moonquakes.\n\nShallow moonquakes are caused when the moon's crust slips and cracks due to the gradual shrinking of the moon when it cools. Meteors can also cause quakes when they crash into the surface of the moon.",
    "People used to believe that kissing a donkey could relieve a toothache.\n\nYep, that’s right!  People have always done rather odd things to prevent toothache. For example, the Ancient Egyptians scrubbed their teeth with a powder made from ox hooves and eggshells. But weirder still, during the Middle Ages in Germany, they thought a cure for a toothache was kissing a donkey. Even if it did something for your toothache, it certainly won't do anything for your breath.",
    "If you open your eyes in a pitch-black room, the colour you'll see is called 'eigengrau'.\n\n‘Eigengrau’ is German for ‘intrinsic grey’, also known as dark light, or brain grey. It is used to describe the uniform dark grey background that many people see in the absence of light. The term dates back to the nineteenth century.",
    "Rabbits can’t vomit.\n\nWelcome to the vomit void. Bunny rabbits are very hygienic creatures who self-groom in much the same way that a cat does. But the rabbit’s digestive system does not move in reverse, meaning rabbits cannot bring up hairballs like a cat can. So basically if you're banking on a burst of bunny barf, don't hold your breath.",
    "Alfred Hitchcock didn’t have a bellybutton.\n\nThe famous director of The Birds and Rear Window was born with one, but after surgery, it vanished after he was sewn back up! ",
    "Bees sometimes sting other bees.\n\nThey don't mean to, but sometimes when they try to defend their nests from intruders, they accidentally sting other bees. Ouch!",
    "There are 32 muscles in a cat’s ear.\n\nThis feature is what allows cats to swivel and rotate their ears so that they can pinpoint the source of a noise. But what's more incredible is that they can move each ear independently and rotate them 180 degrees!",
    "There are more chickens in England than people.\n\nThere are around 982 million chickens eaten each year in the U.K. by 66 million people...  this statistic means that should the chickens decide to take over the country, (a la Jurassic Park) we would be massively outnumbered. The threat is real, people. Come the chicken uprising don't say we didn't warn you.",
    "Crows hold grudges.\n\nA 2011 study revealed crows can remember the human faces of those who capture them. According to another study, ravens, including crows, jays and magpies, can 'hold grudges' for up to two years. So make sure you don't upset a crow, because they just won't let it lie!",
    "‘Hippopotomonstrosesquippedaliophobia' is a fear of long words.",
    "Due to a genetic defect, cats can’t taste sweet things.\n\nThis is because they are missing a taste receptor gene that allows their brains to recognise sweet tastes. No wonder they're often grumpy!",
    "Tornadoes can make it ‘rain’ fish.\n\nThis phenomenon usually happens when swirling whirlwinds over shallow water develop into waterspouts that suck up water and the things living in it, like frogs, eels and fish. The creatures are carried long distances by clouds, and then drop to the ground like a mic.",
]
