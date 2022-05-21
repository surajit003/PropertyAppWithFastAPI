import enum

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Enum

from database import Base


class Carrier(enum.Enum):
    SENDGRID = "SENDGRID"
    TWILIO = "TWILIO"


class MessageType(enum.Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, nullable=False, unique=True, index=True)
    message_type = Column(Enum(MessageType), nullable=False)
    carrier = Column(Enum(Carrier), nullable=False)
    status_code = Column(String, nullable=False)
    response = Column(String, nullable=True)
