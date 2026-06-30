from typing import Optional


def normalize_email(email: str) -> Optional[str]:
    if not email:
        return None

    email = str(email).strip().lower()

    if "@" not in email:
        return None

    domain = email.split("@")[-1]

    if "." not in domain:
        return None

    return email