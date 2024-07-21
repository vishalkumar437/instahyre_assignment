from user.api.serializers import UserSerializer
from user.models import User
from typing import Union
from utils.validators import validate_user_details
from utils.helpers import extract_country_code
from contact_spam.service.service import create_contact
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def user_register_service(request) -> tuple[dict, Union[User, dict]]:
    """
    Service for registering a new user.

    Validates user details, extracts country code, creates the user, 
    and creates an associated contact.

    Returns a tuple with errors (if any) and the user data.
    """
    logger.info("Registering a new user")
    errors = validate_user_details(request)
    user = None
    if len(errors) > 0:
        logger.warning("User validation failed: %s", errors)
        return errors, None
    
    country_code = extract_country_code(request.data.get('phone_number'))
    try:
        user_instance = User(
            name=request.data.get('name'),
            phone_number=request.data.get('phone_number'),
            email=request.data.get('email'),
            country=country_code
        )
        user_instance.set_password(request.data.get('password'))
        user_instance.save()
        user = UserSerializer(user_instance, many=False).data
        create_contact(request)
        logger.info("User created successfully: %s", user)
    except Exception as e:
        logger.error("Error occurred while creating user: %s", e)
        errors['error'] = "Something went wrong while creating User."
        return errors, user

    return errors, user

def user_login_service(request) -> tuple[dict, Union[str, None]]:
    """
    Service for logging in a user.

    Authenticates the user and generates a JWT token.

    Returns a tuple with errors (if any) and the JWT token.
    """
    logger.info("Logging in a user")
    phone = request.data.get('phone_number')
    password = request.data.get('password')

    if not phone or not password:
        logger.warning("Phone number and password are required")
        return {"error": "Phone number and password are required."}, None

    user = authenticate(request, phone_number=phone, password=password)

    if user is None:
        logger.warning("Invalid credentials for phone number: %s", phone)
        return {"error": "Invalid credentials."}, None

    refresh = RefreshToken.for_user(user)
    logger.info("User logged in successfully, token generated")
    return {}, {
        'access': str(refresh.access_token),
    }
