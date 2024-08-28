package org.adriantd.shoppinglist.lists.controller;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.service.CurrentUserService;
import org.adriantd.shoppinglist.lists.dto.ItemRequest;
import org.adriantd.shoppinglist.lists.dto.RegisterItemRequest;
import org.adriantd.shoppinglist.lists.dto.ItemResponse;
import org.adriantd.shoppinglist.lists.service.ItemService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.nio.file.AccessDeniedException;

@RestController
@RequiredArgsConstructor
@RequestMapping("/lists/items")
public class ItemController {

    private final ItemService itemService;
    private final CurrentUserService currentUserService;

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
    public HttpStatus removeItem(@RequestBody ItemRequest itemRequest) {
        try{
            itemService.removeItemFromList(itemRequest,currentUserService.getCurrentUserNickname());
            return HttpStatus.NO_CONTENT;
        }catch (AccessDeniedException e){
            return HttpStatus.FORBIDDEN;
        }catch (Exception e){
            return HttpStatus.NOT_FOUND;
        }
    }

}
