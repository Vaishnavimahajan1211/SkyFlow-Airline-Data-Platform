import string

from python.utils.helpers import generate_code


def test_generate_code_uses_prefix():
    result = generate_code("FL")

    assert result.startswith("FL")


def test_generate_code_default_length():
    result = generate_code("FL")

    assert len(result) == 7


def test_generate_code_custom_length():
    result = generate_code("BK", length=8)

    assert len(result) == 10


def test_generate_code_contains_only_uppercase_letters_and_digits():
    result = generate_code("SF", length=10)

    random_part = result[2:]

    allowed_characters = string.ascii_uppercase + string.digits

    assert all(char in allowed_characters for char in random_part)
