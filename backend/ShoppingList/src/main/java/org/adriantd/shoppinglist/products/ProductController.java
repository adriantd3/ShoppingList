package org.adriantd.shoppinglist.products;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.service.CurrentUserService;
import org.adriantd.shoppinglist.products.dto.ProductRequest;
import org.adriantd.shoppinglist.products.dto.ProductResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.NoSuchElementException;

@RestController
@RequestMapping("/product")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;
    private final CurrentUserService currentUserService;

    @GetMapping("/{id}")
    public ResponseEntity<ProductResponse> getProduct(@PathVariable Integer id){
        try{
            return ResponseEntity.ok(productService.getProduct(id));
        }catch (NoSuchElementException e){
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/user")
    public ResponseEntity<List<ProductResponse>> getUserProducts(){
        return ResponseEntity.ok(productService.getAllUserProducts(currentUserService.getCurrentUserId()));
    }

    @PostMapping("")
    public ResponseEntity<ProductResponse> registerProduct(@RequestBody ProductRequest productRequest){
        return ResponseEntity.ok(productService.registerProduct(productRequest, currentUserService.getCurrentUserId()));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Void> updateProduct(@PathVariable Integer id, @Valid @RequestBody ProductRequest productRequest){
        productService.updateProduct(id, productRequest, currentUserService.getCurrentUserNickname());
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @DeleteMapping("/{id}")
    public HttpStatus deleteProduct(@PathVariable Integer id){
        productService.deleteProduct(id, currentUserService.getCurrentUserNickname());
        return HttpStatus.NO_CONTENT;
    }

}
