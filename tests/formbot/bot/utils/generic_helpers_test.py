import pytest

from formbot.bot.utils.generic_helpers import (
    is_valid_email,
    is_valid_ethiopian_phone_number,
    standardize_phone_number,
)


@pytest.mark.parametrize(
    "phone_number, expected",
    [
        ("+251911223344", True),
        ("0911223344", True),
        ("0711223344", True),
        ("09112233445", False),
        ("+2519112233445", False),
        ("+251911223344", True),
        ("+251911223344", True),
        ("+251911223344", True),
        ("+251911223344", True),
    ],
)
def test_is_valid_ethiopian_phone_number(phone_number, expected):
    # WHEN
    result = is_valid_ethiopian_phone_number(phone_number)

    # THEN
    assert result == expected


@pytest.mark.parametrize(
    "phone_number, expected",
    [
        ("+251911223344", "+251911223344"),
        ("0911223344", "+251911223344"),
        ("0711223344", "+251711223344"),
        ("251911223344", "+251911223344"),
    ],
)
def test_standardize_phone_number(phone_number, expected):
    # WHEN
    result = standardize_phone_number(phone_number)

    # THEN
    assert result == expected


@pytest.mark.parametrize(
    "email, expected",
    [
        ("valid@mail.com", True),
        ("test@example.com", True),
        ("user.name@domain.co", True),
        ("user-name@sub.domain.com", True),
        ("user@domain", False),
        ("user@domain.c", True),
        ("user@domain..com", False),
        ("user@domain@com", False),
        ("@domain.com", False),
        ("user@.com", False),
    ],
)
def test_is_valid_email(email, expected):
    # WHEN
    result = is_valid_email(email)

    # THEN
    assert result == expected
