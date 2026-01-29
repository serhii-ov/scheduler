import re
from fastapi import HTTPException, status


PHONE_REGEX = re.compile(r"^\+?[1-9]\d{7,14}$")
# PHONE_REGEX = re.compile(r"^\+380\d{9}$")         # Original regex for Ukraine only


def normalize_phone(phone: str) -> str:
    """
    Normalize phone number to E.164 format.
    Examples:
    0662017616        → +380662017616
    +380662017616     → +380662017616
    380662017616      → +380662017616
    """
    phone = phone.strip().replace(" ", "").replace("-", "")

    if phone.startswith("0"):
        phone = "+38" + phone[:]

    if not phone.startswith("+"):
        phone = "+" + phone

    if not PHONE_REGEX.match(phone):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid phone number format",
        )

    return phone
