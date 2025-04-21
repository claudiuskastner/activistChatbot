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

from signalbot import Command
from signalbot.context import Context

from contacts.allowed_contacts import allowed

from .ping import PingCommand
from .reminder import ReminderCommand
from .subscription import RegisterCommand


class HelpCommand(Command):
    def describe() -> str:
        return "**.help**: Zeigt diese Nachricht\n**.hilfe**: Zeigt diese Nachricht"

    async def handle(self, context: Context):
        if not allowed(context.message.source):
            return
        command = context.message.text
        if command == ".help" or command == ".hilfe":
            await context.react("🦮")
            help_text = "Hier sind alle Befehle die ich aktuell kann:\n\n"
            for com in COMMANDS:
                help_text += com.describe() + "\n\n"
            await context.send(help_text, text_mode="styled")

            return


COMMANDS: list[Command] = [
    ReminderCommand,
    RegisterCommand,
    PingCommand,
    HelpCommand,
]


def get_commands() -> list[Command]:
    """Returns all registered commands as a list.

    Returns:
        list[Command]: List of registered commands
    """
    return COMMANDS
