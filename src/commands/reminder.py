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

from datetime import datetime

from signalbot import Command
from signalbot.context import Context
from sqlmodel import Session, select

from activist_chatbot.database_management import engine
from events.models import Event


class ReminderCommand(Command):
    def describe() -> str:
        return "**.event** - Listet alle gespeicherten, zukünftigen Veranstaltungen auf."

    async def handle(self, context: Context):
        command = context.message.text
        if command == ".event":
            await context.react("📆")
            with Session(engine) as session:
                statement = select(Event).where(Event.date >= datetime.now())
                results = session.exec(statement)
                for event in results:
                    new_message = f"**{event.title}:**\n{event.date.strftime(' %d. %B %Y %H:%M')} Uhr\n\n{event.location}\n\n{event.link}"  # noqa: E501
                    await context.send(new_message, text_mode="styled")
            return
