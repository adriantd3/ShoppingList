package org.adriantd.shoppinglist.auth.service;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.dao.UserRepository;
import org.adriantd.shoppinglist.auth.dto.AuthResponse;
import org.adriantd.shoppinglist.auth.dto.LoginRequest;
import org.adriantd.shoppinglist.auth.dto.RegisterRequest;
import org.adriantd.shoppinglist.auth.entity.RoleType;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.auth.jwt.JWTService;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.sql.SQLIntegrityConstraintViolationException;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final JWTService jwtService;
    private final AuthenticationManager authenticationManager;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public AuthResponse login(LoginRequest loginRequest) {
        //If authentication fails, an exception will be thrown
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(loginRequest.getNickname(), loginRequest.getPassword()));
        UserDetails userDetails = userRepository.findByNickname(loginRequest.getNickname()).orElseThrow();

        //Once the user is authenticated, a token is generated and sent back to the client
        String token = jwtService.getToken(userDetails);
        return AuthResponse.builder().token(token).build();
    }

    public AuthResponse register(RegisterRequest registerRequest) {
        User user = new User();
        user.setNickname(registerRequest.getNickname());
        user.setName(registerRequest.getName());
        user.setLastname(registerRequest.getLastname());
        user.setEmail(registerRequest.getEmail());
        //The password is encrypted before being stored in the database
        user.setPassword(passwordEncoder.encode(registerRequest.getPassword()));
        user.setRole(RoleType.ROLE_USER);
        user.setPremium((byte) 0);
        userRepository.save(user);

        String token = jwtService.getToken(user);
        return AuthResponse.builder().token(token).build();
    }
}
