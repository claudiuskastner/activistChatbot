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
from datetime import datetime
from urllib.parse import urljoin

import dateparser
import requests
import sqlalchemy
from bs4 import BeautifulSoup, Tag
from sqlmodel import Session

from activist_chatbot.database_management import engine
from activist_chatbot.settings import SCRAPE_URL

from .models import Event


async def fetch_all():
    write_events(scrape_website())


def scrape_website() -> list[dict]:
    try:
        event_page: requests.Response = requests.get(SCRAPE_URL)
        event_page.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return []
    soup = BeautifulSoup(event_page.content, "html.parser")
    cards: list[Tag] = soup.find_all("div", class_="card")
    events: list[dict[str, str | None]] = []
    for card in cards:
        card_link = card.find("a")
        card_date = card.find("div", class_="termin-zeiten")
        event_date = dateparser.parse(card_date.next.get("datetime"), region="DE")
        event_date.replace(tzinfo=datetime.timezone.cet)
        try:
            card_location = card.find("div", class_="termin-ort").get_text(strip=True).replace("Ort:", "")
        except AttributeError:
            card_location = ""
        event = {
            "title": card_link.get_text(strip=True),
            "link": urljoin(SCRAPE_URL, card_link.get("href", "")),
            "date": event_date,
            "time": card_date.find("time", class_="termin-zeiten-uhrzeit").get_text(strip=True),
            "location": card_location,
            "description": card.find("div", class_="card-text").get_text(strip=True),
        }
        if len(event["title"]) < 4:
            break
        events.append(event)

    return events


def write_events(events: list[dict]):
    for event in events:
        d_event = Event(
            title=event.get("title", ""),
            location=event.get("location"),
            link=event.get("link", ""),
            date=event.get("date"),
            time=event.get("time"),
        )
        with Session(engine) as session:
            session.add(d_event)
            with contextlib.suppress(sqlalchemy.exc.IntegrityError):
                session.commit()
