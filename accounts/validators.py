from django.core.exceptions import ValidationError


def phone_number_validator(value):
    if not (value[:3] == '+91' and value[1:].isdigit() and len(value) == 13):
        raise ValidationError('Phone number not valid')
