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
from datetime import datetime

from sqlmodel import Field, SQLModel

from activist_chatbot.database_management import engine


class Event(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str = Field(primary_key=True)
    link: str
    location: str | None
    date: datetime | None = Field(primary_key=True)
    time: str | None


SQLModel.metadata.create_all(engine)
