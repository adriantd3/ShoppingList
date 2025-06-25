package org.adriantd.shoppinglist.websockets;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.dao.UserRepository;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.lists.dao.ItemRepository;
import org.adriantd.shoppinglist.lists.dao.ShopListRepository;
import org.adriantd.shoppinglist.lists.dto.ItemUpdateDTO;
import org.adriantd.shoppinglist.lists.entity.items.Item;
import org.adriantd.shoppinglist.lists.entity.items.ItemId;
import org.adriantd.shoppinglist.lists.entity.lists.Shoplist;
import org.adriantd.shoppinglist.utils.DTOService;
import org.adriantd.shoppinglist.utils.ExceptionMessage;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class LiveListService extends DTOService {

    private final ShopListRepository shopListRepository;
    private final ItemRepository itemRepository;
    private final UserRepository userRepository;

    public void addItem(Integer listId, String username, ItemUpdateDTO itemUpdateDTO) {
        User user = userRepository.findByNickname(username).orElseThrow();
        Shoplist shoplist = shopListRepository.findById(listId).orElseThrow();
        validateUserAuthorization(shoplist, user);


        Item newItem = new Item();
        newItem.setId(new ItemId(listId, itemUpdateDTO.getProductId()));
        newItem.setUser(user);
        newItem.setUnits(itemUpdateDTO.getUnits());
        newItem.setType(itemUpdateDTO.getType());
        newItem.setPurchased(itemUpdateDTO.getPurchased());

        itemRepository.save(newItem);
    }

    public void updateItem(Integer listId, String username, ItemUpdateDTO itemUpdateDTO) {
        User user = userRepository.findByNickname(username).orElseThrow();
        Shoplist shoplist = shopListRepository.findById(listId).orElseThrow();
        validateUserAuthorization(shoplist, user);

        ItemId itemId = new ItemId(listId, itemUpdateDTO.getProductId());
        Item existingItem = itemRepository.findById(itemId)
                .orElseThrow(() -> new IllegalArgumentException("Item not found"));

        existingItem.setUnits(itemUpdateDTO.getUnits());
        existingItem.setType(itemUpdateDTO.getType());
        existingItem.setPurchased(itemUpdateDTO.getPurchased());
        existingItem.setDescription(itemUpdateDTO.getDescription());

        itemRepository.save(existingItem);
    }

    public void deleteItem(Integer listId, String username, ItemUpdateDTO itemUpdateDTO) {
        User user = userRepository.findByNickname(username).orElseThrow();
        Shoplist shoplist = shopListRepository.findById(listId).orElseThrow();
        validateUserAuthorization(shoplist, user);

        ItemId itemId = new ItemId(listId, itemUpdateDTO.getProductId());
        Item existingItem = itemRepository.findById(itemId)
                .orElseThrow(() -> new IllegalArgumentException("Item not found"));

        itemRepository.delete(existingItem);
    }

    private boolean isUserOwner(Shoplist shoplist, User user){
        return shoplist.getUserOwner().getId().equals(user.getId());
    }

    private boolean isUserMember(Shoplist shoplist, User user){
        return shoplist.getUsers().contains(user);
    }

    private void validateUserAuthorization(Shoplist shoplist, User user) {
        if (!isUserOwner(shoplist, user) && !isUserMember(shoplist, user)) {
            throw new AccessDeniedException(ExceptionMessage.USER_NOT_AUTHORIZED_LIST);
        }
    }
}
