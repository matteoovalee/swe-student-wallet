
from smart.auth import authenticate, hash_password, verify_password


def test_password_hashing():
    password = "TestPassword123!"
    stored_hash = hash_password(password)

    assert stored_hash != password
    assert verify_password(password, stored_hash) is True
    assert verify_password("wrong", stored_hash) is False


def test_three_demo_accounts():
    assert authenticate("student@example.com", "StudentDemo2026!") == "student"
    assert authenticate("sponsor@example.com", "SponsorDemo2026!") == "sponsor"
    assert authenticate("admin@example.com", "AdminDemo2026!") == "admin"


def test_invalid_login():
    assert authenticate("admin@example.com", "WrongPassword123!") is None
    assert authenticate("unknown@example.com", "AdminDemo2026!") is None
