from models import payment
from database import SessionLocal
from database import engine

payment.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
