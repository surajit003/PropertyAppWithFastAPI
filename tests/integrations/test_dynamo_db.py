import pytest
from unittest import mock

from aws.services.dynamo_db.logs import create_log, BotoClientException
from tests.integrations.common import read_json


class MockDynamoDbTable:
    def put_item(self, item):
        response = read_json("dynamo_db_response.json")
        return response


@mock.patch("aws.services.dynamo_db.logs.dynamodb.Table")
@mock.patch("aws.services.dynamo_db.logs.boto3.resource")
@pytest.mark.asyncio
async def test_dynamo_db_log(mock_boto3_connect, mock_dynamo_db_table):
    mock_boto3_connect.return_value = "success"
    mock_dynamo_db_table.return_value = MockDynamoDbTable()
    data = {
        "log_id": 12345,
        "request_ip": "localhost",
        "message": {
            "url": "http://127.0.0.1:8000/api/v1/companies/",
            "method": "POST",
            "data": [{"org_id": 1234, "name": "New test"}],
        },
    }
    response = await create_log(data)
    assert response == read_json("dynamo_db_response.json")


@mock.patch("aws.services.dynamo_db.logs.dynamodb.Table")
@mock.patch("aws.services.dynamo_db.logs.boto3.resource")
@pytest.mark.asyncio
async def test_dynamo_db_log_raises_client_error(
    mock_boto3_connect, mock_dynamo_db_table
):
    mock_boto3_connect.return_value = "success"
    mock_dynamo_db_table.side_effect = BotoClientException("Something went wrong")
    data = {
        "log_id": 12345,
        "request_ip": "localhost",
        "message": {
            "url": "http://127.0.0.1:8000/api/v1/companies/",
            "method": "POST",
            "data": [{"org_id": 1234, "name": "New test"}],
        },
    }
    with pytest.raises(BotoClientException) as exc:
        await create_log(data)
    assert isinstance(exc.value, BotoClientException)
    assert exc.value.args[0] == "Something went wrong"
