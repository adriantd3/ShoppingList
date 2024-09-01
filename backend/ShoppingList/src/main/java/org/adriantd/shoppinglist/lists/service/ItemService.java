package org.adriantd.shoppinglist.lists.service;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.dao.UserRepository;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.lists.dao.ItemRepository;
import org.adriantd.shoppinglist.lists.dao.ShopListRepository;
import org.adriantd.shoppinglist.lists.dto.items.ItemRequest;
import org.adriantd.shoppinglist.lists.dto.items.RegisterItemRequest;
import org.adriantd.shoppinglist.lists.dto.items.ItemResponse;
import org.adriantd.shoppinglist.lists.entity.items.Item;
import org.adriantd.shoppinglist.lists.entity.items.ItemId;
import org.adriantd.shoppinglist.lists.entity.lists.Shoplist;
import org.adriantd.shoppinglist.products.dao.ProductRepository;
import org.adriantd.shoppinglist.products.entity.Product;
import org.adriantd.shoppinglist.utils.DTOService;
import org.adriantd.shoppinglist.utils.ExceptionMessage;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.NoSuchElementException;

@Service
@RequiredArgsConstructor
public class ItemService extends DTOService {

    private final ItemRepository itemRepository;
    private final ShopListRepository shopListRepository;
    private final ProductRepository productRepository;
    private final UserRepository userRepository;

    public List<ItemResponse> getAllItemsFromListId(Integer shoplistId) {
        List<Item> items = itemRepository.findAllByShoppingListId(shoplistId);

        return entidadesADTO(items);
    }

    public ItemResponse addItemToList(RegisterItemRequest registerItemRequest, String nickname){
        Shoplist shoplist = shopListRepository.findById(registerItemRequest.getShoplistId()).orElseThrow();
        User user = userRepository.findByNickname(nickname).orElseThrow();

        if(!isUserAllowed(shoplist, user)) {
            throw new AccessDeniedException(ExceptionMessage.USER_NOT_AUTHORIZED_LIST);
        }

        Product product = productRepository.findById(registerItemRequest.getProductId()).orElseThrow();
        ItemId itemId = new ItemId(shoplist.getId(),product.getId());

        if(isItemAlreadyExisting(itemId)){
            throw new AccessDeniedException(ExceptionMessage.ITEM_ALREADY_IN_LIST);
        }

        Item item = new Item();
        item.setId(itemId);
        item.setShoplist(shoplist);
        item.setProduct(product);
        item.setUser(user);
        item.setUnits(registerItemRequest.getUnits());
        item.setType(registerItemRequest.getType());
        item.setPurchased(false);

        itemRepository.save(item);

        return item.toDTO();
    }

    public void removeItemsFromRequest(ItemRequest itemRequest, String nickname) {
        User user = userRepository.findByNickname(nickname).orElseThrow();
        Shoplist shoplist = shopListRepository.findById(itemRequest.getShoplistId()).orElseThrow();
        if(!isUserAllowed(shoplist, user)) {
            throw new AccessDeniedException(ExceptionMessage.USER_NOT_AUTHORIZED_LIST);
        }

        Integer[] productIds = itemRequest.getProductIds();
        for (Integer productId : productIds) {
            removeSingleItem(itemRequest.getShoplistId(), productId);
        }

    }

    private void removeSingleItem(Integer shoplistId, Integer productId){
        ItemId itemId = new ItemId(shoplistId,productId);
        if(!isItemAlreadyExisting(itemId)) {
            throw new NoSuchElementException(ExceptionMessage.ITEM_NOT_FOUND);
        }

        itemRepository.deleteById(itemId);
    }

    public void updateItemsPurchased(ItemRequest itemRequest, String nickname){
        User user = userRepository.findByNickname(nickname).orElseThrow();
        Shoplist shoplist = shopListRepository.findById(itemRequest.getShoplistId()).orElseThrow();
        if(!isUserAllowed(shoplist, user)) {
            throw new AccessDeniedException(ExceptionMessage.USER_NOT_AUTHORIZED_LIST);
        }

        Integer[] productIds = itemRequest.getProductIds();
        for (Integer productId : productIds) {
            updateSingleItemState(shoplist,productId);
        }
    }

    private void updateSingleItemState(Shoplist shoplist, Integer productId)  {
        ItemId itemId = new ItemId(shoplist.getId(),productId);
        if(!isItemAlreadyExisting(itemId)) {
            throw new NoSuchElementException(ExceptionMessage.ITEM_NOT_FOUND);
        }

        Item item = itemRepository.findById(itemId).orElse(null);
        item.setPurchased(!item.getPurchased());

        itemRepository.save(item);
    }

    public void updateItem(@Valid RegisterItemRequest registerItemRequest, String nickname) {
        Shoplist shoplist = shopListRepository.findById(registerItemRequest.getShoplistId()).orElseThrow();
        User user = userRepository.findByNickname(nickname).orElseThrow();

        if(!isUserAllowed(shoplist, user)) {
            throw new AccessDeniedException(ExceptionMessage.USER_NOT_AUTHORIZED_LIST);
        }

        Product product = productRepository.findById(registerItemRequest.getProductId()).orElseThrow();
        ItemId itemId = new ItemId(shoplist.getId(),product.getId());

        if(!isItemAlreadyExisting(itemId)){
            throw new NoSuchElementException(ExceptionMessage.ITEM_NOT_FOUND);
        }

        Item item = itemRepository.findById(itemId).orElseThrow();
        item.setUnits(registerItemRequest.getUnits());
        item.setType(registerItemRequest.getType());

        itemRepository.save(item);

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
