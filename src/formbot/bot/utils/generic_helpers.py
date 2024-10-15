import re


def is_valid_ethiopian_phone_number(phone_number: str) -> bool:
    # Ethiopian phone numbers can start with +251 or 0, followed by either 9, 7, or 1, then 8 more digits.
    pattern = r"^(?:\+?251|0)?[79]\d{8}$"

    if re.match(pattern, phone_number):
        return True

    return False


def standardize_phone_number(phone_number: str) -> str:
    if phone_number.startswith("0"):
        return f"+251{phone_number[1:]}"

    if phone_number.startswith("2"):
        return f"+{phone_number}"

    return phone_number


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if re.match(pattern, email):
        return True

    return False
