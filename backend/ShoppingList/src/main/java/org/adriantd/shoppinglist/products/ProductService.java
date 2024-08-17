package org.adriantd.shoppinglist.products;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.dao.ProductRepository;
import org.adriantd.shoppinglist.dao.UserRepository;
import org.adriantd.shoppinglist.entity.Product;
import org.adriantd.shoppinglist.entity.User;
import org.adriantd.shoppinglist.products.dto.NewProductRequest;
import org.adriantd.shoppinglist.products.dto.ProductResponse;
import org.springframework.stereotype.Service;

import java.time.Instant;

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;
    private final UserRepository userRepository;

    public ProductResponse registerProduct(NewProductRequest newProductRequest, Integer userId) {
        User user = userRepository.findById(userId).orElseThrow();

        Product newProduct = new Product();
        newProduct.setName(newProductRequest.getName());
        newProduct.setImage(newProductRequest.getImage());
        newProduct.setMagnitude(newProductRequest.getMagnitude());
        newProduct.setUser(user);
        newProduct.setTimestamp(Instant.now());

        productRepository.save(newProduct);

        return newProduct.toDTO();
    }
}
