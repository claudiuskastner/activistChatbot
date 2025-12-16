from sqlalchemy.ext.baked import log
import contextlib
import json

import requests
import sqlalchemy
from loguru import logger
from sqlmodel import Session, select

from activist_chatbot.database_management import engine
from activist_chatbot.settings import ALLOWED_GROUPS, PHONE_NUMBER, SIGNAL_SERVICE

from .models import AllowedContact


def scan_contacts():
    for group in ALLOWED_GROUPS:
        res = requests.get(f"http://{SIGNAL_SERVICE}/v1/groups/{PHONE_NUMBER}/{group}")
        try:
            with Session(engine) as session:
                current_allowed_contacts = session.exec(select(AllowedContact)).all()
                existing_contacts: list[str] = []
                for contact in current_allowed_contacts:
                    existing_contacts.append(contact.source)

                if res.status_code == 200:
                    members = json.loads(res.content)["members"]
                    new_members: list[AllowedContact] = []
                    for member in members:
                        if member not in existing_contacts:
                            new_members.append(AllowedContact(source=member))

                    session.bulk_save_objects(new_members)
                    with contextlib.suppress(sqlalchemy.exc.IntegrityError):
                        session.commit()
        except sqlalchemy.exc.SQLAlchemyError as ex:
            return f"Datenbankfehler: {ex!s}"


def allowed(source: str) -> bool:
    try:
        with Session(engine) as session:
            statement = select(AllowedContact).where(AllowedContact.source == source)
            result = session.exec(statement).first()
            logger.debug(f"Allowed contact check for {source}: {result}")
            if result and result.source == source:
                return True
        return False
    except sqlalchemy.exc.SQLAlchemyError:
        return False
    except Exception as ex:
        logger.info(ex)
        return False
