package org.openapitools.api;

import lombok.RequiredArgsConstructor;
import org.openapitools.model.NewProduct;
import org.openapitools.model.Product;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("${openapi.products.base-path:}")
@RequiredArgsConstructor
public class ProductsApiController implements ProductsApi {

    private final ProductsService productsService;

    @Override
    public ResponseEntity<Product> getProduct(Integer id, Integer userId) {
        return ResponseEntity.ok(productsService.getProduct(id, userId));
    }

    @Override
    public ResponseEntity<List<Product>> searchProducts(Integer userId, String name) {
        return ResponseEntity.ok(productsService.searchProduct(userId, name));
    }

    @Override
    public ResponseEntity<Product> postProduct(Integer userId, NewProduct newProduct) {
        return ResponseEntity.ok(productsService.postProduct(userId, newProduct));
    }

    @Override
    public ResponseEntity<Product> putProduct(Integer id, Integer userId, NewProduct newProduct) {
        return ResponseEntity.ok(productsService.updateProduct(id, userId, newProduct));
    }

    @Override
    public ResponseEntity<Void> deleteProduct(Integer id, Integer userId) {
        productsService.deleteProduct(id, userId);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @Override
    public ResponseEntity<Void> checkProduct(Integer id) {
        return productsService.checkProduct(id) ? new ResponseEntity<>(HttpStatus.NO_CONTENT) : new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

}
