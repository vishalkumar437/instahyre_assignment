from .constraints import LENGTH
import re
from .helpers import extract_country_code
from .helpers import get_phone_without_country_code, get_country_code

def clean_phone_number(phone_number: str) -> str:
    """Remove spaces, dashes, and plus signs from phone number."""
    return phone_number.replace(" ", "").replace("-", "").replace("+", "")

def is_valid_digit_sequence(phone_number: str) -> bool:
    """Check if the phone number contains only digits."""
    return phone_number.isdigit()

def is_correct_length(phone_number: str, expected_length: int) -> bool:
    """Check if the phone number has the expected length."""
    return len(phone_number) == expected_length

def matches_pattern(phone_number: str, pattern: str) -> bool:
    """Check if the phone number matches the given regex pattern."""
    return bool(re.match(pattern, phone_number))

def validate_phone_number(phone_number: str) -> str:
    """Validate the format of a phone number."""
    raw_phone_number = get_phone_without_country_code(phone_number)
    if not is_valid_digit_sequence(raw_phone_number):
        return "Phone number should contain only digits."
    if not is_correct_length(raw_phone_number, LENGTH.PHONE_NUMBER):
        return f"Phone number should be {LENGTH.PHONE_NUMBER} digits long."
    if not matches_pattern(raw_phone_number, r'^[6-9]\d{9}$'):
        return "Phone number should start with 6, 7, 8, or 9."
    return "Validated"

def validate_email(email: str) -> bool:
    """Validate the format of an email address."""
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return False
    if len(email) > LENGTH.EMAIL:
        return False
    return True

def validate_user_details(request) -> dict:
    """Validate user details from a request."""
    errors = {}
    phone_number = request.data.get('phone_number')
    if not phone_number:
        return "Phone number is required."
    phone_number = clean_phone_number(phone_number)
    validation_result = validate_phone_number(phone_number)
    if validation_result != "Validated":
        errors['phone_number'] = validation_result
    else:
        country_code = extract_country_code(phone_number)
        if get_country_code(country_code) == 'Unknown Country':
            errors['phone_number'] = "Invalid Country Code."

    if not request.data.get('name'):
        errors['name'] = "Name is required."

    if not validate_email(request.data.get('email')):
        errors['email'] = "Invalid Email."

    return errors