from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException

from settings import HUBSPOT_API_KEY

api_client = HubSpot(api_key=HUBSPOT_API_KEY)


class HubSpotException(Exception):
    pass


class ContactException(HubSpotException):
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
    except ApiException as e:
        raise ContactException(e)
