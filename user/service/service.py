from user.api.serializers import UserSerializer
from user.models import User
from typing import Union
from utils.validators import validate_user_details
from utils.helpers import extract_country_code
from contact_spam.service.service import create_contact
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import logging

def user_register_service(request) -> tuple[dict, Union[User, dict]]:
    errors = validate_user_details(request)
    user = None
    if len(errors) > 0:
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
    except Exception as e:
        print(e)
        errors['error'] = "Something went wrong while creating User."
        return errors, user

    return errors, user

def user_login_service(request) -> tuple[dict, str]:
    phone = request.data.get('phone_number')
    password = request.data.get('password')

    if not phone or not password:
        return {"error": "Phone number and password are required."}, None

    user = authenticate(request, phone_number=phone, password=password)

    if user is None:
        return {"error": "Invalid credentials."}, None

    refresh = RefreshToken.for_user(user)
    return {}, {
        'access': str(refresh.access_token),
    }