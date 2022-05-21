from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud.company import CompanyExistException
from schemas import schema
from hubspot_api import utils
from dependencies.dependencies import get_db
from crud import company as _company

router = APIRouter(
    tags=["company"],
    responses={404: {"description": "Not found"}},
)


@router.post("/companies/")
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


@router.get("/company/{company_name}/")
def get_company(company_name):
    try:
        company = utils.get_company_by_name(company_name)
    except utils.CompanyException as exc:
        raise HTTPException(status_code=200, detail=str(exc))
    return company
