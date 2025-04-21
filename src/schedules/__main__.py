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

import asyncio
from datetime import datetime

import aiocron
import dateutil
from aiocron import Cron
from loguru import logger
from signalbot import SignalBot
from sqlmodel import Session, select

from activist_chatbot.database_management import engine
from activist_chatbot.settings import SCRAPE_CRON_SCHEDULE, SIGNAL_SETTINGS
from contacts.subscriptions import get_user_subscriptions
from events.fetch_events import fetch_all
from events.models import Event

bot = SignalBot(SIGNAL_SETTINGS)


async def send_reminder(phone_number):
    with Session(engine) as session:
        statement = select(Event).where(Event.date >= datetime.now())
        results = session.exec(statement)
        if not results:
            await bot.send(receiver=phone_number, text="Aktuell ist nichts geplant 😴", text_mode="styled")

        for event in results:
            ev_date = ""
            if event.date:
                ev_date = f"\n{event.date.strftime('%d. %B %Y %H:%M Uhr')}"
            new_message = f"**{event.title}:**{ev_date}\n\n{event.location}\n\n{event.link}"
            await bot.send(receiver=phone_number, text=new_message, text_mode="styled")


async def schedule():
    subscriptions: list[dict] = []
    jobs: list[Cron] = []

    logger.info(f"Setting up scrape schedule task. Used interval: {SCRAPE_CRON_SCHEDULE}")
    aiocron.crontab(
        SCRAPE_CRON_SCHEDULE,
        func=fetch_all,
        start=True,
        tz=dateutil.tz.gettz("Europe/Berlin"),
    )

    logger.info("Setting up schedules")
    while True:
        new_subscriptions: list[dict] = get_user_subscriptions()
        if subscriptions != new_subscriptions:
            subscriptions = new_subscriptions
            for job in jobs:
                job.stop()

            for subscription in subscriptions:
                interval_days = subscription["notification_interval"]
                notification_time = subscription["notification_time"]
                phone_number = subscription["phone_number"]

                jobs.append(
                    aiocron.crontab(
                        f"{notification_time.split(':')[1]} {notification_time.split(':')[0]} */{interval_days} * *",
                        func=send_reminder,
                        args=(phone_number,),
                        start=True,
                        tz=dateutil.tz.gettz("Europe/Berlin"),
                    )
                )
        await asyncio.sleep(1)


def main():
    asyncio.run(schedule())


if __name__ == "__main__":
    main()
