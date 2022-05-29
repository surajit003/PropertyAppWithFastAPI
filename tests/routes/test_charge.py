from unittest import mock

import pytest


@mock.patch("logger.log.logger.debug")
@pytest.mark.asyncio
async def test_create_charge(mock_logger_debug, organization, client):
    mock_logger_debug.return_value = "Ok"
    response = client.post(
        "/api/v1/charges/",
        json={
            "currency": "USD",
            "charge_type": "MAINTENANCE",
            "amount": 200,
            "company_name": "Test org",
        },
    )
    assert response.status_code == 201
    assert response.json()["charge_type"] == "maintenance"


@mock.patch("logger.log.logger.debug")
@pytest.mark.asyncio
async def test_create_charge_for_duplicate_charge(
    mock_logger_debug, charge_onboarding, client
):
    mock_logger_debug.return_value = "Ok"
    response = client.post(
        "/api/v1/charges/",
        json={
            "currency": "USD",
            "charge_type": "ONBOARDING",
            "amount": 200,
            "company_name": "Test org",
        },
    )
    assert response.status_code == 200
