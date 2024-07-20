from django.core.exceptions import ObjectDoesNotExist
from contact_spam.models import Contact
from utils.validators import validate_phone_number
from contact_spam.models import Spam
from itertools import chain
from user.models import User
from django.db.utils import IntegrityError

def get_contact_from_name(request):
    """
    Search for a phone number in the contacts given 
    a name in request data.
    """
    name = request.data.get('name')
    if name:
        return list(
            chain(
            Contact.objects.filter(name=name),
            Contact.objects.filter(name__icontains=name)
        ))
    return None
    
        
    
def report_spam_by_phone(request):
    """
    Service with logic for marking phone number
    as spam
    """
    phone_number = request.data.get("phone_number")
    if phone_number is None:
        return {"error":"Phone Number cannot be empty"}, None
    elif validate_phone_number(phone_number) != "Validated":
        return {"error":"Phone Number Not valid"}, None
    try:
        spam_created = Spam.objects.create(phone_number=phone_number, marked_by = request.user)
        if spam_created:
            return None, spam_created
    except IntegrityError as e:
        return {"error": "Phone number already reported spam"}, None


def create_contact(request):
    name = request.data.get("name")
    phone = request.data.get("phone_number")
    email = request.data.get("email")
    if name and phone:
        if validate_phone_number(phone) != "Validated":
            return {"error":"Phone Number is invalid"}, None
        try:
            contact = Contact.objects.create(name = name, phone_number = phone, email = email)
            return None, contact
        except Exception as e:
            return {"error":f"Something went wrong {e}"}, None
    else:
        return {"error":"Phone or Name cannot be empty"}
    
def search_contact_by_phone(query_param):
    
    phone_number = query_param
    if validate_phone_number(phone_number) != "Validated":
        return {"error":"Phone Number is invalid"}, None
    try:
        user = User.objects.get(phone_number=phone_number)
        contacts = Contact.objects.filter(owner=user, phone_number=phone_number).order_by("-pk")
    except ObjectDoesNotExist:
        contacts = Contact.objects.filter(phone_number=phone_number).order_by("-pk")
        print("Contact", contacts)
    return None, contacts
