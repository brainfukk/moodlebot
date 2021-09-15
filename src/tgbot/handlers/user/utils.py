import re


def validate_email(email: str) -> bool:
    pattern = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(pattern, email):
        return False
    return True
