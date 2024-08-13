package org.adriantd.shoppinglist.auth;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Service
public class JWTService {
    private static final String SECRET_KEY="PutoRukai";

    public String getToken(UserDetails userDetails) {
        return this.getToken(new HashMap<String, Object>(), userDetails);
    }

    private String getToken(Map<String,Object> claims, UserDetails userDetails) {
        return Jwts.builder()
                .claims(claims)
                .subject(userDetails.getUsername())
                .issuedAt(new Date(System.currentTimeMillis()))
                .expiration(new Date(System.currentTimeMillis() + 1000 * 60 * 60 * 24))
                .signWith(getSecretKey())
                .compact();
    }

    private SecretKey getSecretKey(){
        byte[] keyBytes= Decoders.BASE64.decode(SECRET_KEY);
        return Keys.hmacShaKeyFor(keyBytes);
    }

    private Claims getClaims(String token){
        return Jwts.parser().verifyWith(getSecretKey()).build().parseSignedClaims(token).getPayload();
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