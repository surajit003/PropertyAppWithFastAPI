from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.orm import Session

from crud.contact import ContactExistException
from crud import contact as _contact
from logger.log import save_log
from schemas import schema
from hubspot_api import utils
from dependencies.dependencies import get_db
from crud import company as _company

router = APIRouter(
    prefix="/api/v1",
    tags=["contact"],
    responses={404: {"description": "Not found"}},
)


@router.post("/contacts/")
@save_log
async def create_contact(
    request: Request, contact: schema.CreateContact, db: Session = Depends(get_db)
):
    db_contact = None
    try:
        org_name = contact.company_name
        db_org = _company.filter_company_by_name(db, org_name).all()[0]
        db_contact = _contact.create_contact(db, contact, db_org.id)
        hubspot_contact = utils.create_contact(data=contact.dict())
    except (utils.ContactException, ContactExistException) as exc:
        if isinstance(exc, utils.ContactException) and db_contact:
            _contact.delete_contact(db, db_contact.id)
        raise HTTPException(status_code=200, detail=str(exc))
    return hubspot_contact


@router.get("/contact/{email}/")
@save_log
async def get_contact(request: Request, email):
    try:
        contact = utils.get_contact_by_email(email)
    except utils.ContactException as exc:
        raise HTTPException(status_code=200, detail=str(exc))
    return contact
