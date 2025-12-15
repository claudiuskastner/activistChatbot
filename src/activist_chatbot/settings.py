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

from typing import cast

import environ

env = environ.Env()
env.prefix = "ACTIVIST_BOT_"
env.read_env(env.str("ENV_PATH", ".env"))  # type: ignore  # noqa: PGH003

# General settings
LOG_LEVEL: str = env.str("LOG_LEVEL", default="INFO")  # type: ignore  # noqa: PGH003
DATABASE_PATH: str = env.str("DATABASE_PATH", default="sqlite:///database.db")  # type: ignore  # noqa: PGH003

# Signal settings
SIGNAL_SERVICE: str = env.str("SIGNAL_SERVICE")  # type: ignore  # noqa: PGH003
PHONE_NUMBER: str = env.str("PHONE_NUMBER")  # type: ignore  # noqa: PGH003
ALLOWED_GROUPS: list[str] = env.list("ALLOWED_GROUPS", default=[])  # type: ignore  # noqa: PGH003
ALLOWED_CONTACTS: list[str] = env.list("ALLOWED_CONTACTS", default=[])  # type: ignore  # noqa: PGH003
SIGNAL_SETTINGS: dict[str, str | None] = {
    "signal_service": SIGNAL_SERVICE,
    "phone_number": PHONE_NUMBER,
}

# Scrape settings
SCRAPE_URL: str = cast(str, env.str("SCRAPE_URL"))
SCRAPE_CRON_SCHEDULE: str = cast(str, env.str("SCRAPE_CRON_SCHEDULE", default="*/60 * * * *"))  # type: ignore[misc]

# Contact settings
CONTACT_SYNC_CRON_SCHEDULE: str = cast(str, env.str("CONTACT_SYNC_CRON_SCHEDULE", default="* * * * *"))  # type: ignore[misc]
