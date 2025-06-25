package org.adriantd.shoppinglist.websockets;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.dao.UserRepository;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.auth.jwt.JWTService;
import org.adriantd.shoppinglist.lists.dao.ShopListRepository;
import org.adriantd.shoppinglist.lists.entity.lists.Shoplist;
import org.adriantd.shoppinglist.lists.service.ListService;
import org.adriantd.shoppinglist.utils.ExceptionMessage;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.simp.stomp.StompCommand;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;
import org.springframework.messaging.support.ChannelInterceptor;
import org.springframework.messaging.support.MessageHeaderAccessor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

import java.security.Principal;

@Component
@RequiredArgsConstructor
public class SubscriberInterceptor implements ChannelInterceptor {

    private final ShopListRepository shopListRepository;
    private final UserRepository userRepository;

    @Override
    public Message<?> preSend(Message<?> message, MessageChannel channel) {
        StompHeaderAccessor accessor = MessageHeaderAccessor.getAccessor(message, StompHeaderAccessor.class);
        if (StompCommand.SUBSCRIBE.equals(accessor.getCommand())){
            UsernamePasswordAuthenticationToken userAuth = (UsernamePasswordAuthenticationToken) accessor.getUser();
            User user = (User) userAuth.getPrincipal();

            if (user == null) {
                throw new IllegalArgumentException(ExceptionMessage.USER_NOT_FOUND);
            }
            String destination = accessor.getDestination();
            if (destination == null || !destination.startsWith("/topic/list/")) {
                throw new IllegalArgumentException(ExceptionMessage.WS_DESTINATION_NOT_FOUND);
            }
            Integer listId = Integer.parseInt(destination.substring("/topic/list/".length()));
            Shoplist shoplist = shopListRepository.findById(listId).orElseThrow();
            if (!shoplist.getUsers().contains(user)) {
                throw new IllegalArgumentException(ExceptionMessage.USER_NOT_AUTHORIZED_LIST);
            }
        }
        return message;
    }
}
