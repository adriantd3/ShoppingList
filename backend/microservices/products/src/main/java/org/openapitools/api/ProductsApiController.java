package org.openapitools.api;

import org.openapitools.dto.NewProduct;
import org.openapitools.dto.Product;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.context.request.NativeWebRequest;

import java.util.List;
import java.util.Optional;
import javax.annotation.Generated;

@Generated(value = "org.openapitools.codegen.languages.SpringCodegen", date = "2025-02-05T18:53:31.285160+01:00[Europe/Madrid]", comments = "Generator version: 7.9.0")
@Controller
@RequestMapping("${openapi.products.base-path:}")
public class ProductsApiController implements ProductsApi {

    private final NativeWebRequest request;

    @Autowired
    public ProductsApiController(NativeWebRequest request) {
        this.request = request;
    }

    @Override
    public Optional<NativeWebRequest> getRequest() {
        return Optional.ofNullable(request);
    }

    @Override
    public ResponseEntity<Product> getProduct(String id, Integer userId) {
        return ProductsApi.super.getProduct(id, userId);
    }

    @Override
    public ResponseEntity<List<Product>> searchProducts(Integer userId) {
        return ProductsApi.super.searchProducts(userId);
    }

    @Override
    public ResponseEntity<Product> postProduct(Integer userId, NewProduct newProduct) {
        return ProductsApi.super.postProduct(userId, newProduct);
    }

    @Override
    public ResponseEntity<Product> putProduct(String id, Integer userId, NewProduct newProduct) {
        return ProductsApi.super.putProduct(id, userId, newProduct);
    }

    @Override
    public ResponseEntity<Void> deleteProduct(String id, Integer userId) {
        return ProductsApi.super.deleteProduct(id, userId);
    }

    @Override
    public ResponseEntity<Void> checkProduct(String id) {
        return new ResponseEntity<>(HttpStatus.NOT_IMPLEMENTED);
    }

}
