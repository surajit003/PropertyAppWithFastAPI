import sqlalchemy.exc
from sqlalchemy.orm import Session

from models import message


class MessageExistException(Exception):
    pass


def create_message(db: Session, message_data):
    db_item = message.Message(**message_data)
    try:
        db.add(db_item)
        db.commit()
    except sqlalchemy.exc.IntegrityError as exc:
        raise MessageExistException(exc.__cause__)
    db.refresh(db_item)
    return db_item
