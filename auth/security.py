import hashlib
import secrets


HASH_ITERATIONS = 100_000


def hash_pin(pin: str) -> str:
    """
    Securely hash a PIN using PBKDF2-HMAC-SHA256.
    """

    if not pin.isdigit():
        raise ValueError("PIN must contain only digits.")

    if len(pin) != 4:
        raise ValueError("PIN must be exactly 4 digits.")

    salt = secrets.token_hex(16)

    pin_hash = hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode("utf-8"),
        salt.encode("utf-8"),
        HASH_ITERATIONS
    )

    return f"{salt}${pin_hash.hex()}"


def verify_pin(pin: str, stored_hash: str) -> bool:
    """
    Verify a PIN against its stored hash.
    """

    try:

        salt, original_hash = stored_hash.split("$")

        pin_hash = hashlib.pbkdf2_hmac(
            "sha256",
            pin.encode("utf-8"),
            salt.encode("utf-8"),
            HASH_ITERATIONS
        )

        return secrets.compare_digest(
            pin_hash.hex(),
            original_hash
        )

    except (ValueError, TypeError):

        return False

def hash_password(password: str) -> str:
    """
    Securely hash an admin password using PBKDF2-HMAC-SHA256.
    """

    if not password or len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters."
        )

    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        HASH_ITERATIONS
    )

    return f"{salt}${password_hash.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify an admin password against its stored hash.
    """

    try:
        salt, original_hash = stored_hash.split("$")

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            HASH_ITERATIONS
        )

        return secrets.compare_digest(
            password_hash.hex(),
            original_hash
        )

    except (ValueError, TypeError):
        return False