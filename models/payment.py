import enum

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class ChargeType(enum.Enum):
    ONBOARDING = "onboarding"
    MAINTENANCE = "maintenance"


class Currency(enum.Enum):
    USD = "USD"
    GBP = "GBP"
    KES = "KES"
    INR = "INR"


class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(String)
    name = Column(String)


class Charge(Base):
    __tablename__ = "charge"

    id = Column(Integer, primary_key=True, index=True)
    currency = Column(Enum(Currency), nullable=False, default=Currency.USD)
    amount = Column(Integer, nullable=False)
    charge_type = Column(Enum(ChargeType), nullable=False)
    org_id = Column(Integer, ForeignKey("organization.id"))
    organization = relationship("Organization", backref="charges")


class Payment(Base):
    __tablename__ = "Payment"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    charge_id = Column(Integer, ForeignKey("charge.id"), nullable=False)
    charge = relationship("Charge", backref="payments")
    response = Column(String, nullable=True)
