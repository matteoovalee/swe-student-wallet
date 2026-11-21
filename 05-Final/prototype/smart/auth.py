import hashlib
import hmac
import secrets
import csv
from pathlib import Path

def hash_password(password):
    salt = secrets.token_bytes(16)
    iterations = 600_000

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations
    )

    return f"pbkdf2_sha256${iterations}${salt.hex()}${hashed.hex()}"



def verify_password(password, stored_hash):
    try:
        algorithm, iterations, salt_hex, hash_hex = stored_hash.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations)
        )

        return hmac.compare_digest(
            actual_hash,
            bytes.fromhex(hash_hex)
        )

    except (ValueError, TypeError, AttributeError):
        return False



def authenticate(email, password):
    users_file = Path(__file__).resolve().parent.parent / "data" / "users.csv"

    with users_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for user in reader:
            if (
                user["email"].strip().lower() == email.strip().lower()
                and verify_password(password, user["password_hash"])
            ):
                return user["role"]

    return None
