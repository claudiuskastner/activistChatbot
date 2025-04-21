import contextlib
import json

import requests
import sqlalchemy
from sqlalchemy import select
from sqlmodel import Session

from activist_chatbot.database_management import engine
from activist_chatbot.settings import ALLOWED_GROUPS, PHONE_NUMBER, SIGNAL_SERVICE

from .models import AllowedContact


def scan_contacts():
    for group in ALLOWED_GROUPS:
        res = requests.get(f"http://{SIGNAL_SERVICE}/v1/groups/{PHONE_NUMBER}/{group}")
        if res.status_code == 200:
            try:
                members = json.loads(res.content)["members"]
                with Session(engine) as session:
                    for member in members:
                        n_member: AllowedContact = AllowedContact(source=member)
                        session.add(n_member)
                    with contextlib.suppress(sqlalchemy.exc.IntegrityError):
                        session.commit()
            except sqlalchemy.exc.SQLAlchemyError as ex:
                return f"Datenbankfehler: {ex!s}"


def allowed(source: str) -> bool:
    try:
        with Session(engine) as session:
            statement = select(AllowedContact).where(AllowedContact.source == source)
            result = session.exec(statement).first()
            if result[0].source == source:
                return True
        return False
    except sqlalchemy.exc.SQLAlchemyError:
        return False
    except Exception:
        return False
