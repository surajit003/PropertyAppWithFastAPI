import sqlalchemy.exc
from sqlalchemy.orm import Session

from models import payment
from schemas.schema import CreateCompany


class CompanyExistException(Exception):
    pass


def create_company(db: Session, company: CreateCompany):
    db_item = payment.Organization(**company.dict())
    try:
        db.add(db_item)
        db.commit()
    except sqlalchemy.exc.IntegrityError as exc:
        raise CompanyExistException(exc.__cause__)
    db.refresh(db_item)
    return db_item


def delete_company(db: Session, organization_id: int):
    db_organization = db.query(payment.Organization).get(organization_id)
    if db_organization:
        db.delete(db_organization)
        db.commit()
        return True
    else:
        return None


def filter_company_by_name(db: Session, company_name: str):
    company = db.query(payment.Organization).filter_by(name=company_name)
    return company
