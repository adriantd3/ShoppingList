from app.modules.sharing.service import hash_share_token


def test_hash_share_token_is_deterministic() -> None:
    token = "same-token-value"
    first = hash_share_token(token)
    second = hash_share_token(token)

    assert first == second
    assert len(first) == 64


def test_hash_share_token_does_not_return_plaintext() -> None:
    token = "plain-token"
    hashed = hash_share_token(token)

    assert hashed != token
