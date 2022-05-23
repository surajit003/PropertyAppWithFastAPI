import os

from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates

from routes.v1 import email
from routes.v1 import contact
from routes.v1 import company
from settings import LOG_FILE

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


@app.on_event("startup")
async def startup_event():
    try:
        os.makedirs(LOG_FILE)
        if not os.path.exists(LOG_FILE):
            os.mknod(LOG_FILE)
    except FileExistsError:
        # directory already exists
        pass
