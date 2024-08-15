package org.adriantd.shoppinglist.auth.config;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.jwt.JWTFilter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class FilterChainConfig {

    private final AuthenticationProvider authenticationProvider;
    private final JWTFilter jwtFilter;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
                .csrf(crsf -> crsf.disable())
                .authorizeHttpRequests(authorizeRequests ->
                        authorizeRequests
                                //Allows auth endpoints to be accessed without authentication
                                //jwtFilter and UsernamePasswordAuthenticationFilter will not be applied to these endpoints
                                .requestMatchers("/auth/**").permitAll()
                                .anyRequest().authenticated()
                ).sessionManagement(sessionManagement ->
                        sessionManagement
                                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)//REST APIs are STATELESS
                ).authenticationProvider(authenticationProvider) //Sets default authentication provider
                //Check for JWT in every request and then
                .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)
                .build();
    }

}
