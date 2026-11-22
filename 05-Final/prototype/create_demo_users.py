
import csv
from getpass import getpass
from pathlib import Path

from smart.auth import hash_password

accounts = [
    ("student@example.com", "student"),
    ("sponsor@example.com", "sponsor"),
    ("admin@example.com", "admin"),
]

users = []

for email, role in accounts:
    password = getpass(f"Create a demo password for {role}: ")

    if not password:
        raise ValueError("Password cannot be empty.")

    users.append({
        "email": email,
        "password_hash": hash_password(password),
        "role": role
    })

file_path = Path(__file__).parent / "data" / "users.csv"

with file_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["email", "password_hash", "role"]
    )
    writer.writeheader()
    writer.writerows(users)

print("Successfully created 3 demo accounts!")
