package org.dutylist.users.api.auth;

import com.google.firebase.FirebaseApp;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import lombok.RequiredArgsConstructor;
import org.dutylist.users.models.response.TokenResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@RequestMapping("/auth")
public class AuthController implements AuthAPI {

    private final AuthService authService;

    @Override
    public ResponseEntity<TokenResponse> validate_token(String token) {
        try {
            TokenResponse response = authService.validateToken(token);
            return ResponseEntity.ok(response);
        } catch (FirebaseAuthException e) {
            return ResponseEntity.status(403).build();
        }
    }
}
