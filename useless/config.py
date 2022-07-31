# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

__all__ = ["Config"]

import os

from dotenv import load_dotenv

if os.path.isfile("config.env"):
    load_dotenv("config.env")

class Config:
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    DEV_USERS = (  # dev list
        838926101,  # @fnixdev <= put your id here
    )
    GP_LOGS = int(os.environ.get("GP_LOGS"))
    DB_URI = os.environ.get("DB_URI")
    TRIGGER = os.environ.get("TRIGGER", "/ ! . :".split())

trg = Config.TRIGGER
