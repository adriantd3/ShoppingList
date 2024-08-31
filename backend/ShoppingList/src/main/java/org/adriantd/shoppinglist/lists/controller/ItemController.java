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
    public ResponseEntity<List<ItemResponse>> getListItems(@PathVariable int id) {
        return ResponseEntity.ok(itemService.getAllItemsFromListId(id));
    }

    @PostMapping("/add")
    public ResponseEntity<ItemResponse> addItem(@RequestBody RegisterItemRequest registerItemRequest) {
        try{
            return ResponseEntity.ok(itemService.addItemToList(registerItemRequest,currentUserService.getCurrentUserNickname()));
        } catch (AccessDeniedException e) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
    }

    @PostMapping("/remove")
    public ResponseEntity<Void> removeItem(@RequestBody ItemRequest itemRequest) {
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
        if(itemRequest == null){
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

}
