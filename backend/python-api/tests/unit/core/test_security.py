from app.core.security import create_access_token, decode_access_token, hash_password, verify_password


def test_password_hashing_roundtrip() -> None:
    hashed = hash_password("StrongPassw0rd!!")
    assert verify_password("StrongPassw0rd!!", hashed)


def test_access_token_roundtrip() -> None:
    token = create_access_token("user-123")
    payload = decode_access_token(token)
    assert payload.sub == "user-123"
