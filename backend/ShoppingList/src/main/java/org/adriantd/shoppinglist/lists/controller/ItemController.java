package org.adriantd.shoppinglist.lists.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.service.CurrentUserService;
import org.adriantd.shoppinglist.lists.dto.items.RegisterItemRequest;
import org.adriantd.shoppinglist.lists.dto.items.ItemResponse;
import org.adriantd.shoppinglist.lists.dto.items.UpdateItemRequest;
import org.adriantd.shoppinglist.lists.service.ItemService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/list/{listId}/item")
public class ItemController {

    private final ItemService itemService;
    private final CurrentUserService currentUserService;

    @GetMapping("")
    public ResponseEntity<List<ItemResponse>> getListItems(@PathVariable int listId) {
        return ResponseEntity.ok(itemService.getAllItemsFromListId(listId));
    }

    @GetMapping("/{itemId}")
    public ResponseEntity<ItemResponse> getItem(@PathVariable int listId, @PathVariable int itemId) {
        return ResponseEntity.ok(itemService.getItemFromList(listId, itemId, currentUserService.getCurrentUserNickname()));
    }

    @PostMapping("")
    public ResponseEntity<ItemResponse> addItem(@PathVariable int listId, @Valid @RequestBody RegisterItemRequest registerItemRequest) {
        return ResponseEntity.ok(itemService.addItemToList(registerItemRequest, listId, currentUserService.getCurrentUserNickname()));
    }

    @DeleteMapping("")
    public ResponseEntity<Void> removeItem(@PathVariable int listId, @RequestParam List<Integer> productId) {
        itemService.removeItemsFromList(listId, productId, currentUserService.getCurrentUserNickname());
        return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
    }

    @PutMapping("")
    public ResponseEntity<Void> updateItem(@PathVariable int listId, @Valid @RequestBody UpdateItemRequest itemRequest) {
        itemService.updateItem(listId, itemRequest, currentUserService.getCurrentUserNickname());
        return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
    }

    @PutMapping("/state")
    public ResponseEntity<Void> updateItemPurchasedState(@PathVariable int listId, @RequestParam List<Integer> productId, @RequestParam boolean purchased) {
        itemService.updateItemsState(listId, productId, purchased, currentUserService.getCurrentUserNickname());
        return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
    }


}
