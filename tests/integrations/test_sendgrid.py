import pytest
from unittest import mock

from email_api.email import send_email
from email_api.email import UnauthorizedException
from email_api.email import BadRequestException
from tests.integrations.common import read_json


@mock.patch("email_api.email.SendGridAPIClient.send")
@pytest.mark.asyncio
async def test_send_email(mock_email_client):
    mock_email_client.return_value = {"status_code": 202}
    response = await send_email(data=read_json("email_data.json"))
    assert response["status_code"] == 202


@mock.patch("email_api.email.SendGridAPIClient.send")
@pytest.mark.asyncio
async def test_send_email_raises_unauthorized_exception(mock_email_client):
    mock_email_client.side_effect = UnauthorizedException("Invalid api key")
    with pytest.raises(UnauthorizedException) as exc:
        await send_email(data=read_json("email_data.json"))
    assert isinstance(exc.value, UnauthorizedException)
    assert exc.value.args[0] == "Invalid api key"


@mock.patch("email_api.email.SendGridAPIClient.send")
@pytest.mark.asyncio
async def test_send_email_raises_bad_request_exception(mock_email_client):
    mock_email_client.side_effect = BadRequestException("Bad request")
    with pytest.raises(BadRequestException) as exc:
        await send_email(data=read_json("email_data.json"))
    assert isinstance(exc.value, BadRequestException)
    assert exc.value.args[0] == "Bad request"
