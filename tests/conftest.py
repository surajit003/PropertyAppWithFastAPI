import pytest

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import create_database
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import schemas.schema
from crud.charge import add_charge
from crud.company import create_company
from crud.contact import create_contact
from crud.message import save_message
from models.message import MessageType
from models.message import Carrier
from models.payment import Organization
from tests.test_database import SQLALCHEMY_DATABASE_URL

from dependencies.dependencies import get_db
from app import app
from database import Base


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    # begin a non-ORM transaction
    connection.begin()
    # bind an individual Session to the connection
    db = Session(bind=connection)
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c


@pytest.fixture
def organization(db):
    yield create_company(
        db, schemas.schema.CreateCompany(name="Test org", org_id=12345)
    )


@pytest.fixture
@pytest.mark.asyncio
async def charge_onboarding(db, organization):
    await add_charge(
        db,
        schemas.schema.CreateCharge(
            company_name="Test org",
            currency="USD",
            charge_type="ONBOARDING",
            amount=200,
        ),
        organization.id,
    )


@pytest.fixture
@pytest.mark.asyncio
async def message(db):
    message_data = dict(
        message_id="123657ab",
        status_code=202,
        message_type=MessageType.EMAIL.value,
        carrier=Carrier.SENDGRID.value,
    )
    await save_message(db, message_data)


@pytest.fixture
def contact(db):
    organization = db.query(Organization).filter_by(name="Test org").all()[0]
    create_contact(
        db,
        schemas.schema.CreateContact(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            phone="2547120202002",
            company_name=organization.name,
        ),
        org_id=organization.id,
    )
