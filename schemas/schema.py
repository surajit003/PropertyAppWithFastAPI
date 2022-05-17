from pydantic import BaseModel
from pydantic import validator


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str


class CreateContact(ContactBase):
    pass
