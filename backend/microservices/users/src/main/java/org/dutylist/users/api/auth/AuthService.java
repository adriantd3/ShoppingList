package org.dutylist.users.api.auth;

import com.google.firebase.FirebaseApp;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import com.google.firebase.auth.FirebaseToken;
import lombok.RequiredArgsConstructor;
import org.dutylist.users.entity.RoleType;
import org.dutylist.users.entity.User;
import org.dutylist.users.models.response.TokenResponse;
import org.dutylist.users.models.response.UserPublicInfo;
import org.dutylist.users.repositories.UserRepository;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.time.Instant;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final FirebaseApp firebaseApp;
    private final UserRepository userRepository;

    public TokenResponse validateToken(String token) throws FirebaseAuthException {
        FirebaseAuth auth = FirebaseAuth.getInstance(firebaseApp);
        FirebaseToken tokenInfo = auth.verifyIdToken(token);

        User user = userRepository.findByEmail(tokenInfo.getEmail());
        if(user == null){
            user = registerNewUser(tokenInfo);
        }

        return generateTokenResponse(token, tokenInfo, user);
    }

    private User registerNewUser(FirebaseToken token){
        User newUser = new User();
        String[] fullName = token.getName().split(" ");

        newUser.setName(fullName[0]);
        newUser.setLastname(token.getName().replace(fullName[0], ""));
        newUser.setEmail(token.getEmail());
        newUser.setPremium(false);
        newUser.setRole(RoleType.ROLE_USER);
        newUser.setImage(token.getPicture());

        userRepository.save(newUser);
        return newUser;
    }

    private TokenResponse generateTokenResponse(String token, FirebaseToken tokenInfo, User user){
        UserPublicInfo userInfo = new UserPublicInfo();
        userInfo.setId(user.getId());
        userInfo.setUsername(user.getName());
        userInfo.setImage(user.getImage());

        TokenResponse response = new TokenResponse();
        Map<String, Object> claims = tokenInfo.getClaims();

        response.setToken(token);
        response.setIat(Instant.ofEpochSecond((Long) claims.get("iat")));
        response.setExp(Instant.ofEpochSecond((Long) claims.get("exp")));
        response.setUser_info(userInfo);

        return response;
    }
}
