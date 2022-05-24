from unittest import mock

import pytest

from hubspot_api.utils import (
    create_contact,
    ContactException,
    create_company,
    CompanyException,
)


class MockHubspotContact:
    def __init__(self, id):
        self.id = id


class MockHubspotCompany:
    def __init__(self, id):
        self.id = id


@mock.patch("hubspot_api.utils.associate_contact_to_organization")
@mock.patch("hubspot_api.utils.get_company_by_name")
@mock.patch("hubspot_api.utils.api_client")
def test_create_contact(
    mock_api_basic_api_create,
    mock_get_company_by_name,
    mock_associate_contact_to_organization,
):
    mock_api_basic_api_create.crm.contacts.basic_api.create.return_value = (
        MockHubspotContact(1234)
    )
    mock_get_company_by_name.return_value = {"id": 1234}
    mock_associate_contact_to_organization.return_value = "ok"
    contact = create_contact(
        dict(
            company_name="Test org",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            phone="111111111",
        )
    )
    assert contact == {"contact_id": 1234}


@mock.patch("hubspot_api.utils.api_client")
def test_create_contact_raises_contact_exception(mock_api_client):
    mock_api_client.crm.contacts.basic_api.create.side_effect = ContactException(
        "Contact Already " "exists"
    )

    with pytest.raises(ContactException) as exc:
        create_contact(
            dict(
                company_name="Test org",
                first_name="Test",
                last_name="User",
                email="testuser@example.com",
                phone="111111111",
            )
        )
    assert isinstance(exc.value, ContactException)
    assert exc.value.args[0] == "Contact Already exists"


@mock.patch("hubspot_api.utils.api_client")
def test_create_company(mock_api_client):
    mock_api_client.crm.companies.basic_api.create.return_value = MockHubspotCompany(
        777
    )
    company = create_company(
        dict(
            name="Test org",
            org_id="999",
        )
    )
    assert company == {"company_id": 777}


@mock.patch("hubspot_api.utils.api_client")
def test_create_company_raises_company_exception(mock_api_client):
    mock_api_client.crm.companies.basic_api.create.side_effect = CompanyException(
        "Company already exists"
    )
    with pytest.raises(CompanyException) as exc:
        create_company(
            dict(
                name="Test org",
                org_id="999",
            )
        )

    assert isinstance(exc.value, CompanyException)
    assert exc.value.args[0] == "Company already exists"
