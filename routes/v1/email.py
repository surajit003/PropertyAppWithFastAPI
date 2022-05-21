from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request

from crud.message import save_message
from crud.message import MessageExistException
from email_api import email
from email_api.email import UnauthorizedException
from email_api.email import BadRequestException
from models.message import MessageType
from models.message import Carrier
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db

router = APIRouter(
    prefix='/api/v1',
    tags=["email"],
    responses={404: {"description": "Not found"}},
)


@router.post("/email/send/")
async def send_email(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        response = await email.send_email(data)
        message = dict(
            message_id=response.headers["x-message-id"],
            status_code=response.status_code,
            message_type=MessageType.EMAIL.value,
            carrier=Carrier.SENDGRID.value,
        )
        await save_message(db, message)
    except (UnauthorizedException, BadRequestException, MessageExistException) as exc:
        raise HTTPException(status_code=200, detail=str(exc))
    return response
