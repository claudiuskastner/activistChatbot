# Copyright (C) 2025 Kastner
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

import pytest

from commands.subscription import parse_subscribe


@pytest.mark.parametrize(
    "command, expected",
    [
        (".abo 3T", {"interval": 3, "time": None}),
        (".abo 3", {"interval": 3, "time": None}),
        (".abo 3 4:00", {"interval": 3, "time": "4:00"}),
        (".abo 3 4:00 Uhr", {"interval": 3, "time": "4:00"}),
        (".abo intervall=3T", {"interval": 3, "time": None}),
        (".abo intervall=3T zeit=18:00", {"interval": 3, "time": "18:00"}),
        (".abo zeit=18:00 intervall=3T", {"interval": 3, "time": "18:00"}),
        (".abo 5T", {"interval": 5, "time": None}),
        (".abo intervall=7T zeit=09:30", {"interval": 7, "time": "09:30"}),
        (".abo 3M", {"error": "Kein gültiges Intervall gefunden."}),
        (".abo", {"error": "No interval provided."}),
        (".abo intervall=ABC", {"error": "Kein gültiges Intervall gefunden."}),
        (".abo zeit=12:00", {"error": "Kein gültiges Intervall gefunden."}),
        (".abo intervall=3T zeit=18:00 Uhr", {"interval": 3, "time": "18:00"}),
        (".abo zeit=18:00 Uhr intervall=3T", {"interval": 3, "time": "18:00"}),
        (".abo intervall=5T zeit=09:30", {"interval": 5, "time": "09:30"}),
        (".abo zeit=20:15 Uhr", {"error": "Kein gültiges Intervall gefunden."}),
        (".abo intervall=3T zeit=4", {"interval": 3, "time": "04:00"}),
        (".abo intervall=3T zeit=18:30", {"interval": 3, "time": "18:30"}),
        (".abo intervall=3T zeit=4 Uhr", {"interval": 3, "time": "04:00"}),
        (".abo intervall=3T", {"interval": 3, "time": None}),
        (".abo zeit=4", {"error": "Kein gültiges Intervall gefunden."}),
        (".abo intervall=3M zeit=4", {"error": "Kein gültiges Intervall gefunden."}),
        (".abo intervall=3T zeit=4:60", {"error": "Ungültige Zeitangabe."}),
    ],
)
def test_parse_subscribe(command, expected):
    assert parse_subscribe(command) == expected
