""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import json
import os
from typing import Callable, TypeVar

from discord.ext import commands


from database import *

T = TypeVar("T")

def not_blacklisted() -> Callable[[T], T]:
    """
    This is a custom check to see if the user executing the command is blacklisted.
    """
    async def predicate(context: commands.Context) -> bool:
        if context.author.id in DatabaseManager.get_blacklisted_users():
            raise UserBlacklisted
        return True

    return commands.check(predicate)