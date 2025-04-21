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

import re

from signalbot import Command
from signalbot.context import Context

from contacts.allowed_contacts import allowed
from contacts.subscriptions import remove_subscription, upsert_subscription


def parse_subscribe(command):
    parts = command.split(" ", 1)
    if len(parts) < 2:
        return {"error": "Kein gültiges Intervall gefunden."}

    params = parts[1].lower().split()
    interval = None
    time = None

    for param in params:
        if re.fullmatch(r"\d+t?", param):
            interval = param.replace("t", "")
        elif re.fullmatch(r"(\d{1,2}:\d{2})(?:\s*uhr)?", param):
            time = param
        elif param.startswith("intervall="):
            match = re.match(r"intervall=(\d+)t", param)
            if match:
                interval = match.group(1)
        elif param.startswith("zeit="):
            match = re.match(r"zeit=(\d{1,2}:\d{2})(?:\s*uhr)?", param)
            if match:
                time = match.group(1)
            else:
                match = re.match(r"zeit=(\d{1,2})", param)
                if match:
                    time = f"{int(match.group(1)):02d}:00"

        if time:
            try:
                hour, minute = map(int, time.split(":"))
                if not (0 <= hour < 24 and 0 <= minute < 60):
                    return {"error": "Ungültige Zeitangabe."}
            except ValueError:
                return {"error": "Ungültige Zeitangabe."}

    if not interval:
        return {"error": "Kein gültiges Intervall gefunden."}

    return {"interval": int(interval), "time": time}


class RegisterCommand(Command):
    def describe() -> str:
        return "**.abo <Tage> <Uhrzeit>** - Registriert dich für regelmäßige Benachrichtigungen.\n\t**.abo 5 16:32**: Du bekommst alle 5 Tage um 16:32 Uhr ein Update.\n**.abo stop**: Du bekommst keine Erinnerungen mehr."  # noqa: E501

    async def handle(self, context: Context):
        if not allowed(context.message.source):
            return
        command = context.message.text
        if command == ".abo stop":
            source = context.message.source
            await context.send(remove_subscription(source))

        elif command.startswith(".abo"):
            new_interval = parse_subscribe(command)

            if "error" in new_interval:
                await context.send(f"Fehler: {new_interval['error']}")
                return

            source = context.message.source

            res: str = upsert_subscription(source, new_interval)
            if res:
                await context.send(res)
                return
            await context.send(
                f"Erfolgreich abonniert! Du bekommst alle {new_interval['interval']} Tage eine Übersicht um {new_interval['time']} Uhr.\nUm das Abo zu beenden, sende **.abo stop**",  # noqa: E501
                text_mode="styled",
            )
