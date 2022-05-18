from fastapi import FastAPI
from fastapi import Request
from fastapi import Depends
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db
from schemas import schema
from hubspot_app import utils

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("charge.html", {"request": request, "name": "surajit"})


@app.post("/contacts")
def create_contact(contact: schema.CreateContact, db: Session = Depends(get_db)):
    try:
        contact = utils.create_contact(data=contact.dict())
    except utils.ContactException as exc:
        raise HTTPException(status_code=200, detail=str(exc))
    return contact


@app.post("/companies")
def create_company(company: schema.CreateCompany):
    try:
        company = utils.create_company(data=company.dict())
    except utils.ContactException as exc:
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
