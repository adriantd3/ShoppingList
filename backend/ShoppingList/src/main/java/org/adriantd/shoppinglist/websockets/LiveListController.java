package org.adriantd.shoppinglist.websockets;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.lists.dto.ItemUpdateDTO;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Controller;

import java.security.Principal;

@Controller
@RequiredArgsConstructor
public class LiveListController {

    private final LiveListService liveListService;

    @MessageMapping("/list/{listId}")
    @SendTo("/topic/list/{listId}")
    public ItemUpdateDTO sendMessage(@DestinationVariable Integer listId, @Payload ItemUpdateDTO message, Principal principal) {
        String username = principal.getName();
        switch (message.getEventType()){
            case ITEM_ADDED -> liveListService.addItem(listId, username, message);
            case ITEM_UPDATED -> liveListService.updateItem(listId, username, message);
            case ITEM_DELETED -> liveListService.deleteItem(listId, username, message);
            default -> throw new IllegalArgumentException("Unknown event type: " + message.getEventType());
        }

        return message;
    }
}
