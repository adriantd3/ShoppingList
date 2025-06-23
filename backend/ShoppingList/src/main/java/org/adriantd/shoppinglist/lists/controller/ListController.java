package org.adriantd.shoppinglist.lists.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.service.CurrentUserService;
import org.adriantd.shoppinglist.lists.dto.lists.ListUpdateRequest;
import org.adriantd.shoppinglist.lists.service.ListService;
import org.adriantd.shoppinglist.lists.dto.lists.ListInfoResponse;
import org.adriantd.shoppinglist.lists.dto.lists.ListRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.security.InvalidParameterException;
import java.util.List;

@RestController
@RequestMapping("/list")
@RequiredArgsConstructor
public class ListController {

    private final ListService listService;
    private final CurrentUserService currentUserService;

    @GetMapping("")
    public ResponseEntity<List<ListInfoResponse>> getAllLists() {
        return ResponseEntity.ok(listService.getListsFromUser(currentUserService.getCurrentUserId()));
    }

    @PostMapping("")
    public ResponseEntity<ListInfoResponse> registerShoplist(@Valid @RequestBody ListRequest request){
        return ResponseEntity.ok(listService.registerShoplist(request, currentUserService.getCurrentUserId()));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteShoplist(@PathVariable Integer id){
        listService.deleteShoplist(id, currentUserService.getCurrentUserId());
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Void> updateShoplist(@PathVariable Integer id, @Valid @RequestBody ListUpdateRequest request){
        listService.updateShoplist(id, request, currentUserService.getCurrentUserId());
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}
