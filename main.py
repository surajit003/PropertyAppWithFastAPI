from fastapi import FastAPI
from fastapi import Request
from fastapi import Depends
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from crud.company import CompanyExistException
from crud.contact import ContactExistException
from dependencies.dependencies import get_db
from schemas import schema
from hubspot_api import utils
from crud import company as _company
from crud import contact as _contact
from routes import email

app = FastAPI()
app.include_router(email.router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        "charge.html", {"request": request, "name": "surajit"}
    )


@app.post("/contacts")
def create_contact(contact: schema.CreateContact, db: Session = Depends(get_db)):
    db_contact = None
    hubspot_contact = None
    try:
        org_name = contact.company_name
        db_org = _company.filter_company_by_name(db, org_name)
        if db_org:
            org = db_org.all()[0]
            db_contact = _contact.create_contact(db, contact, org.id)
            hubspot_contact = utils.create_contact(data=contact.dict())
    except (utils.ContactException, ContactExistException) as exc:
        if isinstance(exc, utils.ContactException) and db_contact:
            _contact.delete_contact(db, db_contact.id)
        raise HTTPException(status_code=200, detail=str(exc))
    return hubspot_contact


@app.post("/companies")
def create_company(company: schema.CreateCompany, db: Session = Depends(get_db)):
    db_company = None
    try:
        db_company = _company.create_company(db, company)
        company = utils.create_company(data=company.dict())
    except (utils.ContactException, CompanyExistException) as exc:
        if isinstance(exc, utils.ContactException) and db_company:
            _company.delete_company(db, db_company.id)
        raise HTTPException(status_code=200, detail=str(exc))
    return company


@app.get("/company/{company_name}/")
def get_company(company_name):
    try:
        company = utils.get_company_by_name(company_name)
    except utils.CompanyException as exc:
        raise HTTPException(status_code=200, detail=str(exc))
    return company


@app.get("/contact/{email}/")
def get_contact(email):
    try:
        contact = utils.get_contact_by_email(email)
    except utils.ContactException as exc:
        raise HTTPException(status_code=200, detail=str(exc))
    return contact
