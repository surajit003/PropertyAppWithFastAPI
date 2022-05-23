import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve(strict=True).parent

DATABASE_HOST = config("DATABASE_HOST")
DATABASE = config("DATABASE_NAME")
DATABASE_USER = config("DATABASE_USER")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_DRIVER = config("DATABASE_DRIVER")
TEST_DATABASE_NAME = config("TEST_DATABASE_NAME")

STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")

HUBSPOT_API_KEY = config("HUBSPOT_API_KEY")

SENDGRID_API_KEY = config("SENDGRID_API_KEY")
WELCOME_MESSAGE_TEMPLATE_ID = config("WELCOME_MESSAGE_TEMPLATE_ID")
PAYMENT_CONFIRMATION_TEMPLATE_ID = config("WELCOME_MESSAGE_TEMPLATE_ID")

TEST_DATA_DIR = BASE_DIR.joinpath('tests/data')
