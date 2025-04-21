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

import uuid

from sqlmodel import Field, SQLModel

from activist_chatbot.database_management import engine


class Contact(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    phone_number: str = Field(primary_key=True)
    notification_interval: int
    notification_time: str
    remind_before: bool


class AllowedContact(SQLModel, table=True):
    source: str = Field(primary_key=True)


SQLModel.metadata.create_all(engine)
