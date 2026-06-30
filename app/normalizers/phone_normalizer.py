import re
from typing import Optional

import phonenumbers

DEFAULT_REGION = "IN"


def normalize_phone(phone: str, region: str = DEFAULT_REGION) -> Optional[str]:

    if not phone:
        return None

    phone = str(phone).strip()

    digits = re.sub(r"\D", "", phone)

    # Indian local number
    if len(digits) == 10:
        digits = "91" + digits

    # Already has Indian country code
    elif len(digits) == 12 and digits.startswith("91"):
        pass

    # Any other length
    else:
        try:
            parsed = phonenumbers.parse(phone, region)

            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(
                    parsed,
                    phonenumbers.PhoneNumberFormat.E164,
                )

            return None

        except Exception:
            return None

    parsed = phonenumbers.parse("+" + digits, None)

    return phonenumbers.format_number(
        parsed,
        phonenumbers.PhoneNumberFormat.E164,
    )