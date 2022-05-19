import sqlalchemy.exc
from sqlalchemy.orm import Session

from models import contact
from schemas.schema import CreateContact


class ContactExistException(Exception):
    pass


def create_contact(db: Session, contact_data: CreateContact, org_id):
    contact_dict = contact_data.dict()
    del contact_dict["company_name"]
    contact_dict["org_id"] = org_id
    db_item = contact.Contact(**contact_dict)
    try:
        db.add(db_item)
        db.commit()
    except sqlalchemy.exc.IntegrityError as exc:
        raise ContactExistException(exc.__cause__)
    db.refresh(db_item)
    return db_item


def delete_contact(db: Session, contact_id):
    db_contact = db.query(contact.Contact).get(contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return True
    else:
        return None
