import json
from unittest import mock

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
def test_email_send(mock_send_email, client, db):
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
