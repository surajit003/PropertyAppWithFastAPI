import os

from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates

from routes.v1 import email
from routes.v1 import contact
from routes.v1 import company
from routes.v1 import charge

app = FastAPI()
app.include_router(email.router)
app.include_router(contact.router)
app.include_router(company.router)
app.include_router(charge.router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "charge.html", {"request": request, "message": "Welcome to Property Management API"}
    )

