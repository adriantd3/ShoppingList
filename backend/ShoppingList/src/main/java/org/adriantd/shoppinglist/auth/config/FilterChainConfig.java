package org.adriantd.shoppinglist.auth.config;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.jwt.JWTFilter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.HttpStatusEntryPoint;
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
                                .requestMatchers("/ws/**", "/ws").permitAll()
                                .requestMatchers("/auth/**").permitAll()
                                .anyRequest().authenticated()
                ).sessionManagement(sessionManagement ->
                        sessionManagement
                                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)//REST APIs are STATELESS
                ).authenticationProvider(authenticationProvider) //Sets default authentication provider
                //Check for JWT in every request. UsernamePasswordAuthentication filter never acts, it is just there to specify order
                .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)
                .exceptionHandling(exceptionHandling ->
                        exceptionHandling
                                .authenticationEntryPoint(new HttpStatusEntryPoint(HttpStatus.NOT_FOUND))
                )
                .build();
    }

}
