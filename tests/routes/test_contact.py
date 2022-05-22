from unittest import mock


@mock.patch("routes.v1.contact.utils.get_contact_by_email")
def test_get_contact_by_email(mock_get_contact_by_email, client):
    mock_get_contact_by_email.return_value = {
        "id": "1234",
        "email": "test@example.com",
        "firstname": "test",
        "lastname": "user",
    }
    response = client.get("/api/v1/contact/abc@example.com")
    assert response.status_code == 200
    assert response.json() == {
        "id": "1234",
        "email": "test@example.com",
        "firstname": "test",
        "lastname": "user",
    }


@mock.patch("routes.v1.contact.utils.create_contact")
@mock.patch("routes.v1.contact._contact.create_contact")
def test_create_contact(
    mock_db_create_contact, mock_hubspot_create_contact, organization, client
):
    mock_db_create_contact.return_value = {
        "first_name": "raaj",
        "last_name": "das",
        "email": "raj@example.com",
        "phone": "+254720323309",
    }
    mock_hubspot_create_contact.return_value = {"contact_id": 12356}
    response = client.post(
        "/api/v1/contacts/",
        json={
            "first_name": "raaj",
            "last_name": "das",
            "email": "test@example.com",
            "phone": "+255720323309",
            "company_name": "Test org",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"contact_id": 12356}
