from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Request
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from dependencies.dependencies import get_db

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/property",
    tags=["onboarding"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{org_id}/charge/", status_code=status.HTTP_201_CREATED)
def onboarding_charge(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("charge.html", {"request": request, "name":"surajit"})
