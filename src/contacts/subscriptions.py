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

import contextlib
import json

import sqlalchemy
from sqlmodel import Session, select

from activist_chatbot.database_management import engine
from contacts.models import Contact


def get_user_subscriptions() -> list[dict]:
    subscriptions: list[dict] = []
    with Session(engine) as session:
        statement = select(Contact)
        results = session.exec(statement)
        for result in results:
            subscriptions.append(json.loads(result.model_dump_json()))
    return subscriptions


def remove_subscription(phone_number: str) -> str:
    with Session(engine) as session:
        try:
            statement = select(Contact).where(Contact.phone_number == phone_number)
            result = session.exec(statement).first()
            if not result:
                return "Du warst gar nicht abonniert! 😩"
            session.delete(result)
            session.commit()
            return "Du bekommst nun keine Nachrichten mehr! 💔"

        except sqlalchemy.exc.SQLAlchemyError as ex:
            return f"Datenbankfehler: {ex!s}"


def upsert_subscription(phone_numer: str, interval: dict[str]) -> str | None:
    with Session(engine) as session:
        try:
            statement = select(Contact).where(Contact.phone_number == phone_numer)
            result = session.exec(statement).first()

            if not result:
                result = Contact()
                result.phone_number = phone_numer

            result.notification_interval = interval["interval"]
            result.remind_before = True
            result.notification_time = interval["time"]
            session.add(result)

            with contextlib.suppress(sqlalchemy.exc.IntegrityError):
                session.commit()

        except sqlalchemy.exc.SQLAlchemyError as ex:
            return f"Datenbankfehler: {ex!s}"
