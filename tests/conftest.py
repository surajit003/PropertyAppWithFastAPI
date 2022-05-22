import pytest

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import create_database
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import schemas.schema
from crud.company import create_company
from crud.contact import create_contact
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
    create_company(db, schemas.schema.CreateCompany(name="Test org", org_id=12345))


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
