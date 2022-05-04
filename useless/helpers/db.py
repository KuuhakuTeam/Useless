# Useless
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Useless/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/Useless/blob/master/LICENSE/>.

__all__ = ["get_collection"]

import asyncio

from motor.core import AgnosticClient, AgnosticCollection, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from . import DB_URI

print("Connecting to Database ...")


_MGCLIENT: AgnosticClient = AsyncIOMotorClient(DB_URI)
_RUN = asyncio.get_event_loop().run_until_complete

if "useless" in _RUN(_MGCLIENT.list_database_names()):
    print("Useless Database Found :) => Now Logging to it...")
else:
    print("Useless Database Not Found :( => Creating New Database...")

_DATABASE: AgnosticDatabase = _MGCLIENT["useless"]


def get_collection(name: str) -> AgnosticCollection:
    """Create or Get Collection from your database"""
    return _DATABASE[name]


def _close_db() -> None:
    _MGCLIENT.close()
