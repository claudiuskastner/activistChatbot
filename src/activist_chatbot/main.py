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

from loguru import logger
from signalbot import SignalBot

from commands import COMMANDS

from .settings import (
    ALLOWED_CONTACTS,
    ALLOWED_GROUPS,
    LOG_LEVEL,
    SIGNAL_SETTINGS,
)

allowed_groups = ALLOWED_GROUPS
allowed_contacts = ALLOWED_CONTACTS

# locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
bot = SignalBot(SIGNAL_SETTINGS)


def main() -> None:
    logger.level(LOG_LEVEL)
    try:
        for bot_command in COMMANDS:
            bot.register(bot_command(), contacts=allowed_contacts, groups=allowed_groups)

        bot.start()

    except KeyboardInterrupt:
        logger.info("Exiting ...")
        sys.exit(0)
