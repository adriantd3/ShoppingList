package org.dutylist.users.api;

import org.dutylist.users.models.request.UserPasswordRequest;
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

    @PostMapping(value = "/userpassword", consumes = "application/json")
    public ResponseEntity<TokenResponse> authenticationUserPassword(@RequestBody UserPasswordRequest userPasswordRequest);

    @PostMapping(value = "/google", consumes = "text/plain")
    public ResponseEntity<TokenResponse> authenticationGoogle(@RequestBody String token);

    @PostMapping(value = "/facebook", consumes = "text/plain")
    public ResponseEntity<TokenResponse> authenticationFacebook(@RequestBody String token);

}
