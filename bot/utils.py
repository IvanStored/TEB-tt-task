import re
from typing import Match


def validate_password(password: str) -> Match[str] | None:
    """
        Validates a password according to the following criteria:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        - Contains at least one special character (!@#$%^&*)
    :param password:
    :return bool
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"

    return re.match(pattern=pattern, string=password)


def validate_age(age: str) -> bool:
    return age.isdigit() and 0 < int(age) <= 100
