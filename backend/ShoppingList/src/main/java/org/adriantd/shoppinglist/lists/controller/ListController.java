package org.adriantd.shoppinglist.lists.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.service.CurrentUserService;
import org.adriantd.shoppinglist.lists.service.ListService;
import org.adriantd.shoppinglist.lists.dto.lists.ListInfoResponse;
import org.adriantd.shoppinglist.lists.dto.lists.ListRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.security.InvalidParameterException;
import java.util.List;

@RestController
@RequestMapping("/lists")
@RequiredArgsConstructor
public class ListController {

    private final ListService listService;
    private final CurrentUserService currentUserService;

    @GetMapping("")
    public ResponseEntity<List<ListInfoResponse>> getAllLists() {
        return ResponseEntity.ok(listService.getListsFromUser(currentUserService.getCurrentUserId()));
    }

    // GET /info?id=1,2,3,4,5
    @GetMapping("/info")
    public ResponseEntity<List<ListInfoResponse>> getListsInfo(@RequestParam("id") List<Integer> shoplistIds) {
        if(shoplistIds == null || shoplistIds.isEmpty()) {
            throw new InvalidParameterException("No shoplist ids provided");
        }

        return ResponseEntity.ok(listService.getListsByIds(shoplistIds));
    }


    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteShoplist(@PathVariable Integer id){
        listService.deleteShoplist(id, currentUserService.getCurrentUserId());
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @PostMapping("/register")
    public ResponseEntity<ListInfoResponse> registerShoplist(@Valid @RequestBody ListRequest request) throws Exception {
        return ResponseEntity.ok(listService.registerShoplist(request, currentUserService.getCurrentUserId()));
    }


    @PutMapping("/update/{id}")
    public ResponseEntity<Void> updateShoplist(@PathVariable Integer id, @RequestParam(value = "name") String name){
        listService.updateShoplist(id, name, currentUserService.getCurrentUserId());
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}
