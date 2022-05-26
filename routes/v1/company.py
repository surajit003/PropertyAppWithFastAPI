from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.orm import Session

from crud.company import CompanyExistException
from logger.log import save_log
from schemas import schema
from hubspot_api import utils
from dependencies.dependencies import get_db
from crud import company as _company

router = APIRouter(
    prefix="/api/v1",
    tags=["company"],
    responses={404: {"description": "Not found"}},
)


@router.post("/companies/")
@save_log
async def create_company(
    request: Request, company: schema.CreateCompany, db: Session = Depends(get_db)
):
    db_company = None
    try:
        db_company = _company.create_company(db, company)
        company = utils.create_company(data=company.dict())
    except (utils.CompanyException, CompanyExistException) as exc:
        if isinstance(exc, utils.CompanyException) and db_company:
            _company.delete_company(db, db_company.id)
        raise HTTPException(status_code=200, detail=str(exc))
    return company


@router.get("/company/{company_name}/")
@save_log
async def get_company(request: Request, company_name):
    try:
        company = utils.get_company_by_name(company_name)
    except utils.CompanyException as exc:
        raise HTTPException(status_code=200, detail=str(exc))
    return company
