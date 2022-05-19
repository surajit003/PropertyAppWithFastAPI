from sqlalchemy import Column, UniqueConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True, index=True)
    active = Column(Boolean, default=False)
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    organization = relationship("Organization", backref="contact")
    UniqueConstraint("org_id", "email", name="contact_email_organization")
