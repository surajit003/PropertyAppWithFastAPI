from unittest import mock

import pytest

from hubspot_api.utils import CompanyException
from hubspot_api.utils import ContactAssociationOrganizationException
from hubspot_api.utils import ContactException
from hubspot_api.utils import create_contact
from hubspot_api.utils import create_company
from hubspot_api.utils import get_contact_by_email
from hubspot_api.utils import get_company_by_name
from hubspot_api.utils import associate_contact_to_organization


class MockHubspotContact:
    def __init__(self, id, properties=None):
        self.id = id
        self.properties = properties


class MockHubspotCompany:
    def __init__(self, id):
        self.id = id


class MockHubspotCompanySearch:
    def __init__(self, results=None):
        self.results = results


class MockHubspotContactSearch:
    def __init__(self, results):
        self.results = results


@mock.patch("hubspot_api.utils.associate_contact_to_organization")
@mock.patch("hubspot_api.utils.get_company_by_name")
@mock.patch("hubspot_api.utils.api_client")
def test_create_contact(
    mock_api_client,
    mock_get_company_by_name,
    mock_associate_contact_to_organization,
):
    mock_api_client.crm.contacts.basic_api.create.return_value = MockHubspotContact(
        1234
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


@mock.patch("hubspot_api.utils.api_client")
def test_get_company_by_name(mock_api_client):
    mock_hubspot_company = MockHubspotCompany(id=1234)
    mock_api_client.crm.companies.search_api.do_search.return_value = (
        MockHubspotCompanySearch(results=[mock_hubspot_company])
    )
    company = get_company_by_name("Test org")
    assert company == {"id": 1234}


@mock.patch("hubspot_api.utils.api_client")
def test_get_company_by_name_with_empty_results(mock_api_client):
    mock_api_client.crm.companies.search_api.do_search.return_value = (
        MockHubspotCompanySearch()
    )
    company = get_company_by_name("Test org1")
    assert company == {}


@mock.patch("hubspot_api.utils.api_client")
def test_get_company_by_name_raises_company_exception(mock_api_client):
    mock_api_client.crm.companies.search_api.do_search.side_effect = CompanyException(
        "Something went wrong"
    )
    with pytest.raises(CompanyException) as exc:
        get_company_by_name("Test org2")

    assert isinstance(exc.value, CompanyException)
    assert exc.value.args[0] == "Something went wrong"


@mock.patch("hubspot_api.utils.api_client")
def test_get_contact_by_email(mock_api_client):
    mock_api_client.crm.contacts.search_api.do_search.return_value = (
        MockHubspotContactSearch(
            results=[
                MockHubspotContact(
                    1234,
                    properties={
                        "email": "abc@example.com",
                        "firstname": "test",
                        "lastname": "user",
                    },
                )
            ],
        )
    )
    contact = get_contact_by_email("abc@example.com")
    assert contact == {
        "id": 1234,
        "email": "abc@example.com",
        "firstname": "test",
        "lastname": "user",
    }


@mock.patch("hubspot_api.utils.api_client")
def test_get_contact_by_email_for_no_result(mock_api_client):
    mock_api_client.crm.contacts.search_api.do_search.return_value = (
        MockHubspotContactSearch(results=None)
    )
    contact = get_contact_by_email("abc1@example.com")
    assert contact == {}


@mock.patch("hubspot_api.utils.api_client")
def test_get_contact_by_email_raises_contact_exception(mock_api_client):
    mock_api_client.crm.contacts.search_api.do_search.side_effect = ContactException(
        "Something went wrong"
    )
    with pytest.raises(ContactException) as exc:
        get_contact_by_email("abc1@example.com")
    assert isinstance(exc.value, ContactException)
    assert exc.value.args[0] == "Something went wrong"


@mock.patch("hubspot_api.utils.api_client")
def test_associate_contact_to_organization(mock_api_client):
    mock_api_client.crm.contacts.associations_api.create.return_value = True
    contact_association = associate_contact_to_organization(
        contact_id=1234, company_id=777
    )
    assert contact_association is True


@mock.patch("hubspot_api.utils.api_client")
def test_associate_contact_to_organization_raises_company_organization_association_exception(
    mock_api_client,
):
    mock_api_client.crm.contacts.associations_api.create.side_effect = (
        ContactAssociationOrganizationException(
            "Something went wrong in linking contact to company"
        )
    )
    with pytest.raises(ContactAssociationOrganizationException) as exc:
        associate_contact_to_organization(contact_id=123, company_id=999)
    assert isinstance(exc.value, ContactAssociationOrganizationException)
    assert exc.value.args[0] == "Something went wrong in linking contact to company"
