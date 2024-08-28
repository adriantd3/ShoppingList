package org.adriantd.shoppinglist.lists.service;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.dao.UserRepository;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.lists.dao.ItemRepository;
import org.adriantd.shoppinglist.lists.dao.ShopListRepository;
import org.adriantd.shoppinglist.lists.dto.ItemRequest;
import org.adriantd.shoppinglist.lists.dto.RegisterItemRequest;
import org.adriantd.shoppinglist.lists.dto.ItemResponse;
import org.adriantd.shoppinglist.lists.entity.Item;
import org.adriantd.shoppinglist.lists.entity.ItemId;
import org.adriantd.shoppinglist.lists.entity.Shoplist;
import org.adriantd.shoppinglist.products.dao.ProductRepository;
import org.adriantd.shoppinglist.products.entity.Product;
import org.springframework.stereotype.Service;

import java.nio.file.AccessDeniedException;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ItemService {

    private final ItemRepository itemRepository;
    private final ShopListRepository shopListRepository;
    private final ProductRepository productRepository;
    private final UserRepository userRepository;

    public ItemResponse addItemToList(RegisterItemRequest registerItemRequest, String nickname) throws Exception {
        Shoplist shoplist = shopListRepository.findById(registerItemRequest.getShoplistId()).orElseThrow();
        User user = userRepository.findByNickname(nickname).orElseThrow();

        if(!isUserAllowed(shoplist, user)) {
            throw new AccessDeniedException("LOG: User not member or owner of the list");
        }

        Product product = productRepository.findById(registerItemRequest.getProductId()).orElseThrow();
        ItemId itemId = new ItemId(shoplist.getId(),product.getId());
        if(isItemAlreadyExisting(itemId)){
            throw new AccessDeniedException("Item is already in list");
        }

        Item item = new Item();
        item.setId(itemId);
        item.setShoplist(shoplist);
        item.setProduct(product);
        item.setUser(user);
        item.setUnits(registerItemRequest.getUnits());
        item.setType(registerItemRequest.getType());

        itemRepository.save(item);

        return item.toDTO();
    }

    public void removeItemFromList(ItemRequest itemRequest, String nickname) throws Exception {
        User user = userRepository.findByNickname(nickname).orElseThrow();
        Shoplist shoplist = shopListRepository.findById(itemRequest.getShoplistId()).orElseThrow();
        if(!isUserAllowed(shoplist, user)) {
            throw new AccessDeniedException("LOG: User not member or owner of the list");
        }

        ItemId itemId = new ItemId(itemRequest.getShoplistId(), itemRequest.getProductId());
        if(!isItemAlreadyExisting(itemId)) {
            throw new AccessDeniedException("LOG: Item does not exist");
        }

        itemRepository.deleteById(itemId);

    }

    /**
     * Checks whether the item already exists in the database
     */
    private boolean isItemAlreadyExisting(ItemId itemId) {
        Item nullItem = itemRepository.findById(itemId).orElse(null);

        return nullItem != null;
    }

    /**
     * Checks whether user is a member or the owner of the list
     */
    private boolean isUserAllowed(Shoplist list, User user){
        List<User> membersList = list.getUsers();
        User owner = list.getUserOwner();

        return membersList.contains(user) || owner.equals(user);
    }


}
