from unittest import mock

from hubspot_api.utils import CompanyException
from models.payment import Organization


@mock.patch("routes.v1.company.utils.get_company_by_name")
def test_company(mock_get_company_by_name, client):
    mock_get_company_by_name.return_value = {"id": 12345}
    response = client.get("/api/v1/company/test-company/")
    assert response.status_code == 200
    assert response.json() == {"id": 12345}


@mock.patch("routes.v1.company.utils.get_company_by_name")
def test_company_for_hubspot_companyexception(mock_get_company_by_name, client):
    mock_get_company_by_name.side_effect = CompanyException(
        "Something went wrong in fetching company from Hubspot"
    )
    response = client.get("/api/v1/company/test-company/")
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Something went wrong in fetching company from Hubspot"
    }


@mock.patch("routes.v1.company.utils.create_company")
def test_create_company(mock_create_company, client):
    mock_create_company.return_value = {"company_id": 1111}
    response = client.post(
        "/api/v1/companies/", json={"org_id": 123, "name": "Warner Bros co"}
    )
    assert response.status_code == 200
    assert response.json() == {"company_id": 1111}


@mock.patch("routes.v1.company.utils.create_company")
def test_create_company_with_hubspot_companyexception(mock_create_company, client, db):
    mock_create_company.side_effect = CompanyException(
        "Something went wrong in creating company in Hubspot"
    )
    response = client.post(
        "/api/v1/companies/", json={"org_id": 123, "name": "Warner Bros co"}
    )
    company = db.query(Organization).filter_by(name="Warner Bros co").all()
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Something went wrong in creating company in Hubspot"
    }
    assert company == []


def test_create_company_with_duplicate_organization_org_id(client, organization):
    response = client.post(
        "/api/v1/companies/", json={"org_id": 12345, "name": "UWISO"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "detail": "duplicate key value violates unique constraint "
        '"organization_org_id_key"\nDETAIL:  Key (org_id)=('
        "12345) already exists.\n"
    }


def test_create_company_with_duplicate_organization_name(client, organization):
    response = client.post(
        "/api/v1/companies/", json={"org_id": 1232245, "name": "Test org"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "detail": "duplicate key value violates unique constraint "
        '"organization_name_key"\nDETAIL:  Key (name)=('
        "Test org) already exists.\n"
    }
