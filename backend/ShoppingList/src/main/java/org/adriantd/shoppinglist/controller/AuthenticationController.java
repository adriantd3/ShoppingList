package org.adriantd.shoppinglist.controller;

import org.adriantd.shoppinglist.dto.AuthResponse;
import org.adriantd.shoppinglist.dto.LoginRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/auth")
public class AuthenticationController {

    public ResponseEntity<AuthResponse> login(LoginRequest loginRequest) {
        return null;
    }
}
