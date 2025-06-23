package org.adriantd.shoppinglist.lists.service;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.dao.UserRepository;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.lists.dao.ItemRepository;
import org.adriantd.shoppinglist.lists.dao.ShopListRepository;
import org.adriantd.shoppinglist.lists.dto.items.RegisterItemRequest;
import org.adriantd.shoppinglist.lists.dto.items.ItemResponse;
import org.adriantd.shoppinglist.lists.dto.items.UpdateItemRequest;
import org.adriantd.shoppinglist.lists.entity.items.Item;
import org.adriantd.shoppinglist.lists.entity.items.ItemId;
import org.adriantd.shoppinglist.lists.entity.lists.Shoplist;
import org.adriantd.shoppinglist.products.dao.ProductRepository;
import org.adriantd.shoppinglist.products.entity.Product;
import org.adriantd.shoppinglist.utils.DTOService;
import org.adriantd.shoppinglist.utils.ExceptionMessage;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.NoSuchElementException;

@Service
@RequiredArgsConstructor
public class ItemService extends DTOService {

    private final ItemRepository itemRepository;
    private final ShopListRepository shopListRepository;
    private final ProductRepository productRepository;
    private final UserRepository userRepository;

    public List<ItemResponse> getAllItemsFromListId(Integer listId) {
        Shoplist shoplist = shopListRepository.findById(listId).orElseThrow();
        User user = userRepository.findByNickname(shoplist.getUserOwner().getNickname()).orElseThrow();
        validateUserAuthorization(shoplist, user);

        List<Item> items = itemRepository.findAllByShoppingListId(listId);

        return entidadesADTO(items);
    }

    public ItemResponse getItemFromList(Integer listId, Integer itemId, String nickname) {
        Shoplist shoplist = shopListRepository.findById(listId).orElseThrow();
        User user = userRepository.findByNickname(nickname).orElseThrow();

        validateUserAuthorization(shoplist, user);

        ItemId itemIdObj = new ItemId(listId, itemId);
        validateItemExistence(itemIdObj);

        Item item = itemRepository.findById(itemIdObj).orElseThrow();

        return item.toDTO();
    }

    @Transactional
    public ItemResponse addItemToList(RegisterItemRequest registerItemRequest, Integer listId ,String nickname){
        Shoplist shoplist = shopListRepository.findById(listId).orElseThrow();
        User user = userRepository.findByNickname(nickname).orElseThrow();

        validateUserAuthorization(shoplist, user);

        Product product = productRepository.findById(registerItemRequest.getProductId()).orElseThrow();
        ItemId itemId = new ItemId(shoplist.getId(),product.getId());

        validateItemExistence(itemId);

        Item item = new Item();
        item.setId(itemId);
        item.setShoplist(shoplist);
        item.setProduct(product);
        item.setUser(user);
        item.setUnits(registerItemRequest.getUnits());
        item.setType(registerItemRequest.getType());
        item.setDescription(registerItemRequest.getDescription());
        item.setPurchased(false);

        itemRepository.save(item);

        return item.toDTO();
    }

    @Transactional
    public void removeItemsFromList(Integer listId, List<Integer> productIds, String nickname) {
        User user = userRepository.findByNickname(nickname).orElseThrow();
        Shoplist shoplist = shopListRepository.findById(listId).orElseThrow();

        validateUserAuthorization(shoplist, user);

        List<ItemId> itemIds = productIds.stream()
                .map(productId -> new ItemId(listId, productId))
                .toList();
        itemRepository.deleteAllById(itemIds);
    }

    private void removeSingleItem(Integer shoplistId, Integer productId){
        ItemId itemId = new ItemId(shoplistId,productId);
        validateItemExistence(itemId);

        itemRepository.deleteById(itemId);
    }

    @Transactional
    public void updateItemsState(Integer listId, List<Integer> productIds, boolean state, String nickname){
        User user = userRepository.findByNickname(nickname).orElseThrow();
        Shoplist shoplist = shopListRepository.findById(listId).orElseThrow();

        validateUserAuthorization(shoplist, user);

        itemRepository.updateItemStateByListAndProductIds(listId, productIds, state);
    }

    private void updateSingleItemState(Shoplist shoplist, Integer productId)  {
        ItemId itemId = new ItemId(shoplist.getId(),productId);
        validateItemExistence(itemId);

        Item item = itemRepository.findById(itemId).orElse(null);
        item.setPurchased(!item.getPurchased());

        itemRepository.save(item);
    }

    @Transactional
    public void updateItem(Integer listId, UpdateItemRequest request, String nickname) {
        Shoplist shoplist = shopListRepository.findById(listId).orElseThrow();
        User user = userRepository.findByNickname(nickname).orElseThrow();

        validateUserAuthorization(shoplist, user);

        Product product = productRepository.findById(request.getProductId()).orElseThrow();
        ItemId itemId = new ItemId(shoplist.getId(),product.getId());

        validateItemExistence(itemId);

        Item item = itemRepository.findById(itemId).orElseThrow();
        item.setUnits(request.getUnits());
        item.setType(request.getType());
        item.setDescription(request.getDescription());

        itemRepository.save(item);

    }

    private void validateUserAuthorization(Shoplist shoplist, User user) {
        if(!isUserAllowed(shoplist, user)) {
            throw new AccessDeniedException(ExceptionMessage.USER_NOT_AUTHORIZED_LIST);
        }
    }

    private void validateItemExistence(ItemId itemId) {
        if(!isItemAlreadyExisting(itemId)) {
            throw new NoSuchElementException(ExceptionMessage.ITEM_NOT_FOUND);
        }
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
