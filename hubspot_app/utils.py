from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm import contacts
from hubspot.crm import companies

from settings import HUBSPOT_API_KEY

api_client = HubSpot(api_key=HUBSPOT_API_KEY)


class HubSpotException(Exception):
    pass


class ContactException(HubSpotException):
    pass


class CompanyException(HubSpotException):
    pass


class ContactAssociationOrganizationException(HubSpotException):
    pass


def create_contact(data):
    try:
        company_name = data["company_name"]
        del data["company_name"]
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
        contact_id = contact.id
        company = get_company_by_name(company_name)
        company_id = company["id"]
        associate_contact_to_organization(contact_id, company_id)
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
    except companies.exceptions.ApiException as e:
        raise CompanyException(e)


def get_company_by_name(name):
    email_filter = companies.Filter(property_name="name", operator="EQ", value=name)
    filter_group = companies.FilterGroup(filters=[email_filter])
    request = contacts.PublicObjectSearchRequest(
        filter_groups=[
            filter_group,
        ],
        properties=[
            "id",
        ],
    )
    try:
        company = api_client.crm.companies.search_api.do_search(request)
        if company.results:
            company_detail = company.results[0]
            return {
                "id": company_detail.id,
            }
        else:
            return {}
    except companies.exceptions.ApiException as e:
        raise CompanyException(e)


def get_contact_by_email(email):
    email_filter = contacts.Filter(property_name="email", operator="EQ", value=email)
    filter_group = contacts.FilterGroup(filters=[email_filter])
    request = contacts.PublicObjectSearchRequest(
        filter_groups=[
            filter_group,
        ],
    )
    try:
        contact = api_client.crm.contacts.search_api.do_search(request)
        if contact.results:
            contact_detail = contact.results[0]
            return {
                "id": contact_detail.id
            }
        else:
            return {}
    except contacts.exceptions.ApiException as e:
        raise ContactException(e)


def associate_contact_to_organization(contact_id, company_id):
    try:
        api_client.crm.contacts.associations_api.create(
            contact_id=contact_id,
            to_object_type="company",
            to_object_id=company_id,
            association_type="contact_to_company",
        )
    except contacts.exceptions.ApiException as e:
        raise ContactAssociationOrganizationException(e)
    return True
