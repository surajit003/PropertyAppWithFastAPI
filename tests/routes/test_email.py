import json
from unittest import mock

from email_api.email import UnauthorizedException
from email_api.email import BadRequestException
from models.message import Message
from settings import TEST_DATA_DIR


def read_json(filename):
    with open(TEST_DATA_DIR.joinpath(filename)) as resp_file:
        return json.load(resp_file)


class SendGridResponseMock:
    def __init__(self, headers, status_code):
        self.headers = headers
        self.status_code = status_code


@mock.patch("routes.v1.email.email.send_email")
@mock.patch("logger.log.logger.debug")
def test_email_send(mock_logger_debug, mock_send_email, client, db):
    mock_logger_debug.return_value = "Ok"
    sendgrid_response_mock = SendGridResponseMock(
        headers={"x-message-id": "xvis10203sn"}, status_code=202
    )
    mock_send_email.return_value = sendgrid_response_mock
    response = client.post("/api/v1/email/send/", json=read_json("email_data.json"))
    message = db.query(Message).filter_by(message_id="xvis10203sn").all()[0]
    assert response.status_code == 200
    assert message.message_id == "xvis10203sn"
    assert message.message_type.value == "EMAIL"
    assert message.status_code == "202"
    assert message.carrier.value == "SENDGRID"


@mock.patch("routes.v1.email.email.send_email")
@mock.patch("logger.log.logger.debug")
def test_email_send_with_sendgrid_unauthorizedexception(mock_logger_debug, mock_send_email, client):
    mock_logger_debug.return_value = "Ok"
    mock_send_email.side_effect = UnauthorizedException("Not allowed to access the API")
    response = client.post("/api/v1/email/send/", json=read_json("email_data.json"))
    assert response.status_code == 200
    assert response.json() == {"detail": "Not allowed to access the API"}


@mock.patch("routes.v1.email.email.send_email")
@mock.patch("logger.log.logger.debug")
def test_email_send_with_sendgrid_bad_request_exception(mock_logger_debug, mock_send_email, client):
    mock_logger_debug.return_value = "Ok"
    mock_send_email.side_effect = BadRequestException("Bad request")
    response = client.post("/api/v1/email/send/", json=read_json("email_data.json"))
    assert response.status_code == 200
    assert response.json() == {"detail": "Bad request"}


@mock.patch("routes.v1.email.email.send_email")
@mock.patch("logger.log.logger.debug")
def test_email_send_with_db_duplicate_message_id(
        mock_logger_debug, mock_send_email, client, message
):
    mock_logger_debug.return_value = "Ok"
    sendgrid_response_mock = SendGridResponseMock(
        headers={"x-message-id": "123657ab"}, status_code=202
    )
    mock_send_email.return_value = sendgrid_response_mock
    response = client.post("/api/v1/email/send/", json=read_json("email_data.json"))
    assert response.status_code == 200
    assert response.json() == {
        "detail": "duplicate key value violates unique constraint "
                  '"ix_message_message_id"\nDETAIL:  Key (message_id)=('
                  "123657ab) already exists.\n"
    }
