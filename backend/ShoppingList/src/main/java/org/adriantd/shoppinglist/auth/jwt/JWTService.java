package org.adriantd.shoppinglist.auth.jwt;

import io.github.cdimascio.dotenv.Dotenv;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Service
public class JWTService {

    private final SecretKey SECRET_KEY;

    public JWTService(){
        Dotenv dotenv = Dotenv.load();
        String base64Key = dotenv.get("SECRET_KEY");
        byte[] keyBytes = Base64.getDecoder().decode(base64Key);
        this.SECRET_KEY = new SecretKeySpec(keyBytes, "HmacSHA256");
    }

    public String getToken(UserDetails userDetails) {
        return this.getToken(new HashMap<String, Object>(), userDetails);
    }

    private String getToken(Map<String,Object> claims, UserDetails userDetails) {
        System.out.println(SECRET_KEY.toString());
        return Jwts.builder()
                .claims(claims)
                .subject(userDetails.getUsername())
                .issuedAt(new Date(System.currentTimeMillis()))
                .expiration(new Date(System.currentTimeMillis() + 1000 * 60 * 60 * 24)) //24h
                .signWith(SECRET_KEY)
                .compact();
    }

    private Claims getClaims(String token){
        return Jwts.parser().verifyWith(SECRET_KEY).build().parseSignedClaims(token).getPayload();
    }

    public String getUsernameFromToken(String token){
        return getClaims(token).getSubject();
    }

    public boolean isTokenValid(String token, UserDetails userDetails) {
        String expectedUsername = userDetails.getUsername();
        String actualUsername = getUsernameFromToken(token);
        return expectedUsername.equals(actualUsername) && !isTokenExpired(token);
    }

    public boolean isTokenExpired(String token) {
        Date expiration = getClaims(token).getExpiration();
        return expiration.before(new Date());
    }
}
