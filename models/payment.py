import enum
import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import UniqueConstraint
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
    org_id = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)


class Charge(Base):
    __tablename__ = "charge"
    __table_args__ = (UniqueConstraint("org_id", "charge_type"),)
    id = Column(Integer, primary_key=True, index=True)
    currency = Column(Enum(Currency), nullable=False, default=Currency.USD)
    amount = Column(Integer, nullable=False)
    charge_type = Column(Enum(ChargeType), nullable=False)
    org_id = Column(Integer, ForeignKey("organization.id"))
    organization = relationship("Organization", backref="charges")
    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, default=datetime.datetime.now)


class Payment(Base):
    __tablename__ = "Payment"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    charge_id = Column(Integer, ForeignKey("charge.id"), nullable=False)
    charge = relationship("Charge", backref="payments")
    response = Column(String, nullable=True)
