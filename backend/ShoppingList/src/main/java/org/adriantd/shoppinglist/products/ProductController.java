package org.adriantd.shoppinglist.products;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.service.CurrentUserService;
import org.adriantd.shoppinglist.products.dto.ProductRequest;
import org.adriantd.shoppinglist.products.dto.ProductResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.nio.file.AccessDeniedException;
import java.util.NoSuchElementException;

@RestController
@RequestMapping("/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;
    private final CurrentUserService currentUserService;

    @PostMapping("/register")
    public ResponseEntity<ProductResponse> registerProduct(@RequestBody ProductRequest productRequest) throws Exception {
        return ResponseEntity.ok(productService.registerProduct(productRequest, currentUserService.getCurrentUserId()));
    }

    @PutMapping("/update/{id}")
    public HttpStatus updateProduct(@PathVariable Integer id, @RequestBody ProductRequest productRequest) throws Exception {
        try{
            productService.updateProduct(id, productRequest, currentUserService.getCurrentUserNickname());
            return HttpStatus.OK;
        } catch (NoSuchElementException e) {
            return HttpStatus.NOT_FOUND;
        } catch (AccessDeniedException e) {
            return HttpStatus.FORBIDDEN;
        }
    }

    @DeleteMapping("/delete/{id}")
    public HttpStatus deleteProduct(@PathVariable Integer id) throws Exception {
        try{
            productService.deleteProduct(id, currentUserService.getCurrentUserNickname());
            return HttpStatus.OK;
        } catch (NoSuchElementException e) {
            return HttpStatus.NOT_FOUND;
        } catch (AccessDeniedException e) {
            return HttpStatus.FORBIDDEN;
        }
    }

}
