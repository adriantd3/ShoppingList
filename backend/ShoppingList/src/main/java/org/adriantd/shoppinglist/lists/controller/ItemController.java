package org.adriantd.shoppinglist.lists.controller;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.service.CurrentUserService;
import org.adriantd.shoppinglist.lists.dto.items.ItemRequest;
import org.adriantd.shoppinglist.lists.dto.items.RegisterItemRequest;
import org.adriantd.shoppinglist.lists.dto.items.ItemResponse;
import org.adriantd.shoppinglist.lists.service.ItemService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.nio.file.AccessDeniedException;
import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/lists/items")
public class ItemController {

    private final ItemService itemService;
    private final CurrentUserService currentUserService;

    @GetMapping("/{id}")
    public ResponseEntity<List<ItemResponse>> getListItems(@PathVariable(required = false) int id) {
        if(id <= 0){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }

        return ResponseEntity.ok(itemService.getAllItemsFromListId(id));
    }

    @PostMapping("/add")
    public ResponseEntity<ItemResponse> addItem(@RequestBody(required = false) RegisterItemRequest registerItemRequest) {
        if (!isValidRegisterItemRequest(registerItemRequest)) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }

        try{
            return ResponseEntity.ok(itemService.addItemToList(registerItemRequest,currentUserService.getCurrentUserNickname()));
        } catch (AccessDeniedException e) {
            //Error on permissions
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        } catch (Exception e) {
            //Any entity not found
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
    }

    @PostMapping("/remove")
    public ResponseEntity<Void> removeItem(@RequestBody(required = false) ItemRequest itemRequest) {
        if (!isValidItemRequest(itemRequest)) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }

        try{
            itemService.removeItemsFromRequest(itemRequest,currentUserService.getCurrentUserNickname());
            return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
        }catch (AccessDeniedException e){
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        }catch (Exception e){
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
    }

    @PutMapping("/state")
    public ResponseEntity<Void> updateItemPurchasedState(@RequestBody(required = false) ItemRequest itemRequest) {
        if(!isValidItemRequest(itemRequest)){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }

        try{
            itemService.updateItemsPurchased(itemRequest, currentUserService.getCurrentUserNickname());
            return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
        }catch (AccessDeniedException e){
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        }catch (Exception e){
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
    }

    private boolean isValidItemRequest(ItemRequest itemRequest){
        return itemRequest != null && itemRequest.getShoplistId() != null && itemRequest.getProductIds() != null;
    }

    private boolean isValidRegisterItemRequest(RegisterItemRequest registerItemRequest){
        return registerItemRequest != null
                && registerItemRequest.getShoplistId() != null
                && registerItemRequest.getProductId() != null
                && registerItemRequest.getUnits() != null
                && registerItemRequest.getType() != null;
    }
}
