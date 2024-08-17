package org.adriantd.shoppinglist.products;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.service.CurrentUserService;
import org.adriantd.shoppinglist.products.dto.NewProductRequest;
import org.adriantd.shoppinglist.products.dto.ProductResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;
    private final CurrentUserService currentUserService;

    @PostMapping("/register")
    public ResponseEntity<ProductResponse> registerProduct(@RequestBody NewProductRequest newProductRequest) throws Exception {
        return ResponseEntity.ok(productService.registerProduct(newProductRequest, currentUserService.getCurrentUserId()));
    }
}
