package org.adriantd.shoppinglist.auth;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.dao.RoleRepository;
import org.adriantd.shoppinglist.dao.UserRepository;
import org.adriantd.shoppinglist.dto.AuthResponse;
import org.adriantd.shoppinglist.dto.LoginRequest;
import org.adriantd.shoppinglist.dto.RegisterRequest;
import org.adriantd.shoppinglist.entity.Role;
import org.adriantd.shoppinglist.entity.User;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final JWTService jwtService;
    private final AuthenticationManager authenticationManager;
    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;

    public AuthResponse login(LoginRequest loginRequest) {
        //If authentication fails, an exception will be thrown
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(loginRequest.getEmail(), loginRequest.getPassword()));
        UserDetails userDetails = userRepository.findByEmail(loginRequest.getEmail()).orElseThrow();

        //Once the user is authenticated, a token is generated and sent back to the client
        String token = jwtService.getToken(userDetails);
        return AuthResponse.builder().token(token).build();
    }

    @Transactional
    public AuthResponse register(RegisterRequest registerRequest) {
        User user = new User();
        Role role = roleRepository.findById(1).orElseThrow();
        role.setId(1);
        user.setName(registerRequest.getName());
        user.setLastname(registerRequest.getLastname());
        user.setEmail(registerRequest.getEmail());
        //The password is encrypted before being stored in the database
        user.setPassword(passwordEncoder.encode(registerRequest.getPassword()));
        user.setRole(role);
        user.setPremium((byte) 0);
        userRepository.save(user);

        String token = jwtService.getToken(user);
        return AuthResponse.builder().token(token).build();
    }
}
