from pydantic import BaseModel
from pydantic import validator


class CompanyBase(BaseModel):
    org_id: str
    org_name:str


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str


class CreateContact(ContactBase):
    pass


class CreateCompany(CompanyBase):
    pass