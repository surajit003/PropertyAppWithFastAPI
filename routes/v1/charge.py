from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from sqlalchemy.orm import Session

from crud.charge import ChargeExistException
from crud.company import filter_company_by_name
from logger.log import save_log
from dependencies.dependencies import get_db
from crud import charge as _charge
from schemas.schema import CreateCharge

router = APIRouter(
    prefix="/api/v1",
    tags=["charge"],
    responses={404: {"description": "Not found"}},
)


@router.post("/charges/", status_code=status.HTTP_201_CREATED)
@save_log
async def create_charge(request: Request, charge: CreateCharge, db: Session = Depends(get_db)):
    try:
        company_name = charge.company_name
        company = filter_company_by_name(db, company_name).all()[0]
        response = await _charge.add_charge(db, charge, company.id)
    except ChargeExistException as exc:
        raise HTTPException(status_code=200, detail=str(exc))
    return response
