from unittest import mock

from hubspot_api.utils import ContactException
from models.contact import Contact


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


def test_create_contact_returns_duplicate_email_error(organization, contact, client):
    response = client.post(
        "/api/v1/contacts/",
        json={
            "first_name": "raaj",
            "last_name": "das",
            "email": "testuser@example.com",
            "phone": "2547120202002",
            "company_name": "Test org",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "detail": "duplicate key value violates unique constraint "
        '"contact_email_key"\nDETAIL:  Key (email)=('
        "testuser@example.com) already exists.\n"
    }


@mock.patch("routes.v1.contact._contact.delete_contact")
@mock.patch("routes.v1.contact.utils.create_contact")
def test_create_contact_raises_hubspot_contactexception(
    mock_create_contact, mock_delete_contact, organization, client
):
    mock_create_contact.side_effect = ContactException(
        "Email with this contact exists " "in Hubspot"
    )
    mock_delete_contact.return_value = True
    response = client.post(
        "/api/v1/contacts/",
        json={
            "first_name": "test",
            "last_name": "user",
            "email": "testuser1@example.com",
            "phone": "2547120202002",
            "company_name": "Test org",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Email with this contact exists in Hubspot"}


@mock.patch("routes.v1.contact.utils.create_contact")
def test_create_contact_rollbacks_db_contact_for_hubspot_exception(
    mock_create_contact, db, organization, client
):
    mock_create_contact.side_effect = ContactException(
        "Email with this contact exists " "in Hubspot"
    )
    response = client.post(
        "/api/v1/contacts/",
        json={
            "first_name": "test",
            "last_name": "user",
            "email": "testuser2@example.com",
            "phone": "2547120202002",
            "company_name": "Test org",
        },
    )
    contact = db.query(Contact).filter_by(email="testuser2@example.com").all()
    assert response.status_code == 200
    assert response.json() == {"detail": "Email with this contact exists in Hubspot"}
    assert contact == []
