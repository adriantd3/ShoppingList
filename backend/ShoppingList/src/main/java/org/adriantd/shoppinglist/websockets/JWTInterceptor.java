package org.adriantd.shoppinglist.websockets;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.jwt.JWTService;
import org.adriantd.shoppinglist.utils.ExceptionMessage;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.simp.stomp.StompCommand;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;
import org.springframework.messaging.support.ChannelInterceptor;
import org.springframework.messaging.support.MessageBuilder;
import org.springframework.messaging.support.MessageHeaderAccessor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class JWTInterceptor implements ChannelInterceptor {

    private final JWTService jwtService;
    private final UserDetailsService userDetailsService;

    @Override
    public Message<?> preSend(Message<?> message, MessageChannel channel) {

        StompHeaderAccessor accessor = MessageHeaderAccessor.getAccessor(message, StompHeaderAccessor.class);
        if (StompCommand.CONNECT.equals(accessor.getCommand())){
            String token = accessor.getFirstNativeHeader("Authorization");
            String username;
            if (token == null) {
                throw new IllegalArgumentException(ExceptionMessage.JWT_TOKEN_REQUIRED);
            }
            token = token.substring(7); // Remove "Bearer " prefix
            username = jwtService.getUsernameFromToken(token);
            if(username == null) {
                throw new IllegalArgumentException(ExceptionMessage.INVALID_JWT_TOKEN);
            }

            UserDetails userDetails = userDetailsService.loadUserByUsername(username);
            if(jwtService.isTokenInvalid(token, userDetails)) {
                throw new IllegalArgumentException(ExceptionMessage.INVALID_JWT_TOKEN);
            }
            if(jwtService.isTokenExpired(token)) {
                throw new IllegalArgumentException(ExceptionMessage.JWT_TOKEN_EXPIRED);
            }

            UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
            accessor.setUser(authToken);
        }
        return MessageBuilder.createMessage(message.getPayload(), accessor.getMessageHeaders());
    }
}
