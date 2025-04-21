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

from signalbot import Command, Context

from contacts.allowed_contacts import allowed


class PingCommand(Command):
    def describe() -> str:
        return "**ping**: Das ist ein Test ob das Bot responsive ist."

    async def handle(self, context: Context):
        if not allowed(context.message.source):
            return
        command = context.message.text

        if command == "ping":
            await context.react("🏓")
            await context.send("🏓 pong")
            return
