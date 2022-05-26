import sqlalchemy.exc
from sqlalchemy.orm import Session

from models import payment

class ChargeExistException(Exception):
    pass


async def add_charge(db: Session, charge):
    try:
        db_item = payment.Charge(**charge)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    except sqlalchemy.exc.IntegrityError as exc:
        raise ChargeExistException(exc)
    return db_item
