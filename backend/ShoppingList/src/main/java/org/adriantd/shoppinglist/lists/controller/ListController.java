package org.adriantd.shoppinglist.lists.controller;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.service.CurrentUserService;
import org.adriantd.shoppinglist.lists.service.ListService;
import org.adriantd.shoppinglist.lists.dto.ListInfoResponse;
import org.adriantd.shoppinglist.lists.dto.ListRequest;
import org.adriantd.shoppinglist.lists.dto.ListUpdateRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.nio.file.AccessDeniedException;

@RestController
@RequestMapping("/lists")
@RequiredArgsConstructor
public class ListController {

    private final ListService listService;
    private final CurrentUserService currentUserService;

    @PostMapping("/register")
    public ResponseEntity<ListInfoResponse> registerShoplist(@RequestBody ListRequest request) throws Exception {
        return ResponseEntity.ok(listService.registerShoplist(request, currentUserService.getCurrentUserId()));
    }

    @DeleteMapping("/{id}")
    public HttpStatus deleteShoplist(@PathVariable Integer id){
        try {
            listService.deleteShoplist(id, currentUserService.getCurrentUserId());
            return HttpStatus.NO_CONTENT;
        } catch (AccessDeniedException e) {
            return HttpStatus.FORBIDDEN;
        } catch (Exception e) {
            return HttpStatus.NOT_FOUND;
        }
    }

    @PutMapping("/update/{id}")
    public HttpStatus updateShoplist(@PathVariable Integer id, @RequestBody ListUpdateRequest request){
        try {
            listService.updateShoplist(id, request, currentUserService.getCurrentUserId());
            return HttpStatus.OK;
        } catch (AccessDeniedException e) {
            return HttpStatus.FORBIDDEN;
        } catch (Exception e) {
            return HttpStatus.NOT_FOUND;
        }
    }
}
