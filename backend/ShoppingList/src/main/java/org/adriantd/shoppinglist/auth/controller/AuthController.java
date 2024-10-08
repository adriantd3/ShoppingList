package org.adriantd.shoppinglist.auth.controller;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.service.AuthService;
import org.adriantd.shoppinglist.auth.dto.AuthResponse;
import org.adriantd.shoppinglist.auth.dto.LoginRequest;
import org.adriantd.shoppinglist.auth.dto.RegisterRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody LoginRequest loginRequest) {
        try{
            return ResponseEntity.ok(authService.login(loginRequest));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
    }

    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@RequestBody RegisterRequest registerRequest) {
        try{
            return ResponseEntity.ok(authService.register(registerRequest));
        }catch (Exception e){
            return ResponseEntity.status(HttpStatus.CONFLICT).build();
        }
    }

}
