from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput

from settings import HUBSPOT_API_KEY

api_client = HubSpot(api_key=HUBSPOT_API_KEY)


class HubSpotException(Exception):
    pass


class ContactException(HubSpotException):
    pass


class CompanyException(HubSpotException):
    pass


def create_contact(data):
    try:
        contact_map = {
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "email",
            "phone": "phone",
        }

        data = {contact_map[k]: v for k, v in data.items()}
        simple_public_object_input = SimplePublicObjectInput(
            properties=data
        )
        contact = api_client.crm.contacts.basic_api.create(
            simple_public_object_input=simple_public_object_input
        )
        return {"contact_id": contact.id}
    except hubspot.crm.contacts.exceptions.ApiException as e:
        raise ContactException(e)


def create_company(data):
    # company == organization
    try:
        company_map = {
            "org_id": "companynumber",
            "org_name": "name",
        }

        data = {company_map[k]: v for k, v in data.items()}
        simple_public_object_input = SimplePublicObjectInput(
            properties=data
        )
        company = api_client.crm.companies.basic_api.create(
            simple_public_object_input=simple_public_object_input
        )
        return {"company_id": company.id}
    except hubspot.crm.companies.exceptions.ApiException as e:
        raise CompanyException(e)
