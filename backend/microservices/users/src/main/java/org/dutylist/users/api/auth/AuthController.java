package org.dutylist.users.api.auth;

public class AuthController implements AuthAPI {

    @Override
    public ResponseEntity<TokenResponse> validate_token(String token) {
        return null;
    }
}
