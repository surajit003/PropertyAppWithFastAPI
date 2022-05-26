import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.orm import Session

from crud.charge import ChargeExistException
from crud.company import filter_company_by_name
from logger.log import save_log
from dependencies.dependencies import get_db
from crud import charge as _charge

router = APIRouter(
    prefix="/api/v1",
    tags=["charge"],
    responses={404: {"description": "Not found"}},
)


@router.post("/charges/")
@save_log
async def create_charge(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        company_name = data["company_name"]
        company = filter_company_by_name(db, company_name).all()[0]
        company_data = dict(
            currency=data["currency"],
            amount=data["amount"],
            charge_type=data["charge_type"],
            org_id=company.id,
            created_at=datetime.datetime.now(),
        )
        response = await _charge.add_charge(db, company_data)
    except ChargeExistException as exc:
        raise HTTPException(status_code=200, detail=str(exc))
    return response
