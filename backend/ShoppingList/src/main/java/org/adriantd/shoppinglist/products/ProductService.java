package org.adriantd.shoppinglist.products;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.dao.ProductRepository;
import org.adriantd.shoppinglist.dao.UserRepository;
import org.adriantd.shoppinglist.entity.Product;
import org.adriantd.shoppinglist.entity.User;
import org.adriantd.shoppinglist.products.dto.ProductRequest;
import org.adriantd.shoppinglist.products.dto.ProductResponse;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.net.http.HttpResponse;
import java.nio.file.AccessDeniedException;
import java.time.Instant;
import java.util.NoSuchElementException;

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;
    private final UserRepository userRepository;

    public ProductResponse registerProduct(ProductRequest productRequest, Integer userId) {
        User user = userRepository.findById(userId).orElseThrow();

        Product newProduct = new Product();
        newProduct.setName(productRequest.getName());
        newProduct.setImage(productRequest.getImage());
        newProduct.setMagnitude(productRequest.getMagnitude());
        newProduct.setUser(user);
        newProduct.setTimestamp(Instant.now());

        productRepository.save(newProduct);

        return newProduct.toDTO();
    }

    public void updateProduct(Integer id, ProductRequest productRequest, String nickname) throws Exception {
        Product product = productRepository.findById(id).orElseThrow(NoSuchElementException::new);

        if (!product.getUser().getNickname().equals(nickname)) {
            throw new AccessDeniedException("LOG: User is not the owner of the product");
        }

        product.setName(productRequest.getName());
        product.setImage(productRequest.getImage());
        product.setMagnitude(productRequest.getMagnitude());

        productRepository.save(product);
    }

    public void deleteProduct(Integer id, String nickname) throws Exception {
        Product product = productRepository.findById(id).orElseThrow(NoSuchElementException::new);

        if (!product.getUser().getNickname().equals(nickname)) {
            throw new AccessDeniedException("LOG: User is not the owner of the product");
        }

        productRepository.delete(product);
    }
}
