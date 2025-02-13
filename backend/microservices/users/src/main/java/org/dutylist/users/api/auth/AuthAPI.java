package org.dutylist.users.api.auth;

import org.dutylist.users.models.response.TokenResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Validated
@RequestMapping("/auth")
public interface AuthAPI {

    @PostMapping(consumes = "text/plain")
    public ResponseEntity<TokenResponse> validate_token(@RequestBody String token);

}
