import enum
import python_http_client
import sendgrid
from sendgrid.helpers.mail import *

import settings


class SendgridException(Exception):
    pass


class UnauthorizedException(SendgridException):
    pass


class BadRequestException(SendgridException):
    pass


class EmailType(enum.Enum):
    WELCOME_EMAIL = "welcome_template"
    PAYMENT_EMAIL = "payment_template"


def generate_message(data):
    templates = {
        "welcome_template": settings.WELCOME_MESSAGE_TEMPLATE_ID,
        "payment_template": settings.PAYMENT_CONFIRMATION_TEMPLATE_ID,
    }
    recipient_message = []
    recipients = data["recipients"]
    for recipient in recipients:
        recipient_message.append(
            To(
                email=recipient["recipient_email"],
                name=recipient["recipient_name"],
                dynamic_template_data=data["template_content"],
            ),
        )
    message = Mail(
        from_email=data["sender"],
        to_emails=recipient_message,
        subject=data["subject"],
    )
    email_type = data["email_type"]
    message.template_id = templates[email_type]
    return message


def send_email(data):
    message = generate_message(data)
    try:
        sendgrid_client = sendgrid.SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sendgrid_client.send(message)
    except python_http_client.exceptions.UnauthorizedError as e:
        raise UnauthorizedException(e)
    except python_http_client.exceptions.BadRequestsError as e:
        raise BadRequestException(e)
    return response
