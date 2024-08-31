package org.adriantd.shoppinglist.lists.controller;

import jakarta.validation.Valid;
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
    public ResponseEntity<ItemResponse> addItem(@Valid @RequestBody RegisterItemRequest registerItemRequest){
        return ResponseEntity.ok(itemService.addItemToList(registerItemRequest, currentUserService.getCurrentUserNickname()));
    }

    @PostMapping("/remove")
    public ResponseEntity<Void> removeItem(@Valid @RequestBody ItemRequest itemRequest) {
        itemService.removeItemsFromRequest(itemRequest, currentUserService.getCurrentUserNickname());
        return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
    }

    @PutMapping("/state")
    public ResponseEntity<Void> updateItemPurchasedState(@Valid @RequestBody ItemRequest itemRequest) {
        itemService.updateItemsPurchased(itemRequest, currentUserService.getCurrentUserNickname());
        return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
    }

}
