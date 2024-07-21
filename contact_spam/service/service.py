import logging
from django.core.exceptions import ObjectDoesNotExist
from contact_spam.models import Contact, Spam
from utils.validators import validate_phone_number
from itertools import chain
from user.models import User
from django.db.utils import IntegrityError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_contact_from_name(request):
    """
    Search for a phone number in the contacts given 
    a name in request data.
    """
    logger.info("Searching for contact by name")
    name = request.data.get('name')
    if name:
        logger.debug("Name provided: %s", name)
        contacts = list(
            chain(
                Contact.objects.filter(name=name),
                Contact.objects.filter(name__icontains=name)
            )
        )
        logger.info("Contacts found: %d", len(contacts))
        return contacts
    logger.warning("Name not provided in request")
    return None

def report_spam_by_phone(request):
    """
    Service with logic for marking phone number
    as spam
    """
    logger.info("Reporting phone number as spam")
    phone_number = request.data.get("phone_number")
    if phone_number is None:
        logger.warning("Phone Number cannot be empty")
        return {"error":"Phone Number cannot be empty"}, None
    elif validate_phone_number(phone_number) != "Validated":
        logger.warning("Phone Number Not valid: %s", phone_number)
        return {"error":"Phone Number Not valid"}, None
    try:
        spam_created = Spam.objects.create(phone_number=phone_number, marked_by=request.user)
        if spam_created:
            logger.info("Spam reported successfully for phone number: %s", phone_number)
            # Also update is_spam field in Contact model
            contacts = Contact.objects.filter(phone_number=phone_number)
            for contact in contacts:
                contact.is_spam = True
                contact.save()
            return None, spam_created
    except IntegrityError as e:
        logger.error("Phone number already reported as spam: %s", phone_number)
        return {"error": "Phone number already reported spam"}, None

def create_contact(request):
    logger.info("Creating a new contact")
    name = request.data.get("name")
    phone = request.data.get("phone_number")
    email = request.data.get("email")
    if name and phone:
        logger.debug("Name: %s, Phone: %s, Email: %s", name, phone, email)
        if validate_phone_number(phone) != "Validated":
            logger.warning("Invalid phone number: %s", phone)
            return {"error":"Phone Number is invalid"}, None
        try:
            contact = Contact.objects.create(name=name, phone_number=phone, email=email)
            logger.info("Contact created successfully: %s", contact)
            return None, contact
        except Exception as e:
            logger.error("Error occurred while creating contact: %s", e)
            return {"error":f"Something went wrong {e}"}, None
    else:
        logger.warning("Phone or Name cannot be empty")
        return {"error":"Phone or Name cannot be empty"}

def search_contact_by_phone(query_param):
    logger.info("Searching for contact by phone number")
    phone_number = query_param
    if validate_phone_number(phone_number) != "Validated":
        logger.warning("Invalid phone number: %s", phone_number)
        return {"error":"Phone Number is invalid"}, None
    try:
        user = User.objects.get(phone_number=phone_number)
        contacts = Contact.objects.filter(owner=user, phone_number=phone_number).order_by("-pk")
        logger.info("Contacts found for user: %s", user)
    except ObjectDoesNotExist:
        contacts = Contact.objects.filter(phone_number=phone_number).order_by("-pk")
        logger.info("Contacts found: %d", len(contacts))
    except Exception as e:
        logger.error("Error occurred: %s", e)
        return {"error": str(e)}, None
    return None, contacts