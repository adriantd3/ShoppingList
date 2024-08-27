package org.adriantd.shoppinglist.products;

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
@RequestMapping("/products")
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
    public ResponseEntity<List<ProductResponse>> getUserProducts() throws Exception{
        return ResponseEntity.ok(productService.getAllUserProducts(currentUserService.getCurrentUserId()));
    }

    @PostMapping("/register")
    public ResponseEntity<ProductResponse> registerProduct(@RequestBody ProductRequest productRequest) throws Exception {
        return ResponseEntity.ok(productService.registerProduct(productRequest, currentUserService.getCurrentUserId()));
    }

    @PutMapping("/update/{id}")
    public HttpStatus updateProduct(@PathVariable Integer id, @RequestBody ProductRequest productRequest){
        try{
            productService.updateProduct(id, productRequest, currentUserService.getCurrentUserNickname());
            return HttpStatus.OK;
        } catch (NoSuchElementException e) {
            return HttpStatus.NOT_FOUND;
        } catch (Exception e) {
            return HttpStatus.FORBIDDEN;
        }
    }

    @DeleteMapping("/delete/{id}")
    public HttpStatus deleteProduct(@PathVariable Integer id){
        try{
            productService.deleteProduct(id, currentUserService.getCurrentUserNickname());
            return HttpStatus.NO_CONTENT;
        } catch (NoSuchElementException e) {
            return HttpStatus.NOT_FOUND;
        } catch (Exception e) {
            return HttpStatus.FORBIDDEN;
        }
    }

}
