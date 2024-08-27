package org.adriantd.shoppinglist.lists;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.service.CurrentUserService;
import org.adriantd.shoppinglist.lists.dto.ListInfoResponse;
import org.adriantd.shoppinglist.lists.dto.ListRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

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
}
