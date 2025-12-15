# Copyright (C) 2025 Claudius Kastner
#
# This file is part of activistChatbot.
#
# activistChatbot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import sys
import asyncio

from loguru import logger
from signalbot import SignalBot

from commands import COMMANDS

from .settings import (
    ALLOWED_CONTACTS,
    ALLOWED_GROUPS,
    LOG_LEVEL,
    SIGNAL_SETTINGS,
)

allowed_groups: list[str] = ALLOWED_GROUPS
allowed_contacts: list[str] = ALLOWED_CONTACTS


async def main() -> None:
    logger.level(LOG_LEVEL)
    try:
        bot = SignalBot(SIGNAL_SETTINGS)

        for bot_command in COMMANDS:
            bot.register(bot_command)

        bot.start(run_forever=False)

        await asyncio.Event().wait()

    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Exiting ...")
        sys.exit(0)
