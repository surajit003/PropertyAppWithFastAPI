import sqlalchemy.exc
from sqlalchemy.orm import Session

from models import payment


class ChargeExistException(Exception):
    pass


async def add_charge(db: Session, charge, org_id: int):
    try:
        charge_dict = charge.dict()
        del charge_dict["company_name"]
        charge_dict["org_id"] = org_id
        db_item = payment.Charge(**charge_dict)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    except sqlalchemy.exc.IntegrityError as exc:
        raise ChargeExistException(exc)
    return db_item
