from fastapi import FastAPI
from fastapi import Request
from fastapi import Depends
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from crud.company import CompanyExistException
from dependencies.dependencies import get_db
from schemas import schema
from hubspot_api import utils
from crud import company as _company
from routes import email
from routes import contact
from routes import company

app = FastAPI()
app.include_router(email.router)
app.include_router(contact.router)
app.include_router(company.router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "charge.html", {"request": request, "message": "Welcome to Property Management API"}
    )
