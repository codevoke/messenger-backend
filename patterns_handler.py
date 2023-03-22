import re
from configuration import pattern as pattern

config_data = {
    'nickname': [pattern.nickname_pattern, pattern.nickname_min_length, pattern.nickname_max_length],
    'password': [pattern.password_pattern, pattern.password_min_length, pattern.password_max_length],
    'email': [pattern.email_pattern, pattern.email_min_length, pattern.email_max_length],
    'phone': [pattern.phone_number_pattern, pattern.phone_number_min_length, pattern.phone_number_max_length]
}
FIELD_NICKNAME = "nickname"
FIELD_PASSWORD = "password"
FIELD_EMAIL = "email"
FIELD_PHONE = "phone"
FIELDS = [FIELD_PHONE, FIELD_EMAIL, FIELD_PASSWORD, FIELD_NICKNAME]


def validate_data(text: str, field: str):
    if field not in FIELDS:
        return False, "incorrect_field-name"
    if not valid_length_of_str(text=text, min_length=config_data[field][1], max_length=config_data[field][2]):
        return False, "length_error"
    if not valid_str_with_pattern(config_data[field][0], text):
        return False, "content_error"
    return True


def valid_str_with_pattern(text_pattern: str, text: str):
    return bool(re.match(text_pattern, str(text)))


def valid_length_of_str(text: str, min_length: int = 0, max_length: int = 1):
    if min_length <= len(text) <= max_length:
        return True
    return False


if __name__ == "__main__":
    print(validate_data('1', 'password'))
