package org.adriantd.shoppinglist.auth.jwt;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.utils.ExceptionMessage;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;

@Component
@RequiredArgsConstructor
public class JWTFilter extends OncePerRequestFilter {

    private final JWTService jwtService;
    private final UserDetailsService userDetailsService;

    private static final List<AntPathRequestMatcher> EXCLUDED_PATHS = List.of(
            new AntPathRequestMatcher("/auth/**"),
            new AntPathRequestMatcher("/ws/**")
    );

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) throws ServletException {
        return EXCLUDED_PATHS.stream()
                .anyMatch(matcher -> matcher.matches(request));
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {

        String token = getTokenFromRequest(request);
        if (token == null) {
            sendError(response, ExceptionMessage.JWT_TOKEN_REQUIRED);
            return;
        }

        String username;
        try {
            username = jwtService.getUsernameFromToken(token);
        } catch (RuntimeException e) {
            sendError(response, ExceptionMessage.INVALID_JWT_TOKEN);
            return;
        }

        if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = userDetailsService.loadUserByUsername(username);

            if(jwtService.isTokenInvalid(token, userDetails)) {
                sendError(response, ExceptionMessage.INVALID_JWT_TOKEN);
                return;
            }

            if(jwtService.isTokenExpired(token)) {
                sendError(response, ExceptionMessage.JWT_TOKEN_EXPIRED);
                return;
            }

            UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
            authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
            SecurityContextHolder.getContext().setAuthentication(authToken);
        }

        filterChain.doFilter(request, response);
    }

    private String getTokenFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (bearerToken != null && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }

    private void sendError(HttpServletResponse response, String message) throws IOException {
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        response.setContentType("application/json");
        response.getWriter().write("{\"error\": \"Authentication error: " + message + "\"," +
                "\"status\": 401}");
    }
}
