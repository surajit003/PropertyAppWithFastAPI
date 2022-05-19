from pydantic import BaseModel
from pydantic import validator


class CompanyBase(BaseModel):
    org_id: str
    name: str


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str


class CreateContact(ContactBase):
    company_name: str


class CreateCompany(CompanyBase):
    pass
