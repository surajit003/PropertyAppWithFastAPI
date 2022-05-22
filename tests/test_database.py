from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dependencies.dependencies import get_db
from app import app
from settings import DATABASE_DRIVER
from settings import DATABASE_USER
from settings import DATABASE_PASSWORD
from settings import DATABASE_HOST
from settings import TEST_DATABASE_NAME

SQLALCHEMY_DATABASE_URL = f"{DATABASE_DRIVER}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{TEST_DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
