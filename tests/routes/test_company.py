from unittest import mock

from hubspot_api.utils import CompanyException


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
