import python_http_client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import To
from sendgrid.helpers.mail.mail import Mail
import settings


class SendgridException(Exception):
    pass


class UnauthorizedException(SendgridException):
    pass


class BadRequestException(SendgridException):
    pass


def generate_message(data):
    templates = {
        "welcome_email": settings.WELCOME_MESSAGE_TEMPLATE_ID,
        "payment_email": settings.PAYMENT_CONFIRMATION_TEMPLATE_ID,
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
        sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sendgrid_client.send(message)
    except python_http_client.exceptions.UnauthorizedError as e:
        raise UnauthorizedException(e)
    except python_http_client.exceptions.BadRequestsError as e:
        raise BadRequestException(e)
    return response
