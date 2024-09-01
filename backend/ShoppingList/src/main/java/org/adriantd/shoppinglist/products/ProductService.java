package org.adriantd.shoppinglist.products;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.products.dao.ProductRepository;
import org.adriantd.shoppinglist.auth.dao.UserRepository;
import org.adriantd.shoppinglist.products.entity.Product;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.products.dto.ProductRequest;
import org.adriantd.shoppinglist.products.dto.ProductResponse;
import org.adriantd.shoppinglist.utils.DTOService;
import org.adriantd.shoppinglist.utils.ExceptionMessage;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductService extends DTOService {

    private final ProductRepository productRepository;
    private final UserRepository userRepository;

    public ProductResponse getProduct(Integer productId){
        Product product = productRepository.findById(productId).orElseThrow();

        return product.toDTO();
    }

    public List<ProductResponse> getAllUserProducts(Integer userId){
        List<Product> userProducts = productRepository.findAllByUserId(userId).orElse(new ArrayList<>());

        return entidadesADTO(userProducts);
    }

    @Transactional
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

    @Transactional
    public void updateProduct(Integer id, ProductRequest productRequest, String nickname) {
        Product product = productRepository.findById(id).orElseThrow();

        if (!product.getUser().getNickname().equals(nickname)) {
            throw new AccessDeniedException(ExceptionMessage.USER_NOT_AUTHORIZED_PRODUCT);
        }

        product.setName(productRequest.getName());
        product.setImage(productRequest.getImage());
        product.setMagnitude(productRequest.getMagnitude());

        productRepository.save(product);
    }

    @Transactional
    public void deleteProduct(Integer id, String nickname) {
        Product product = productRepository.findById(id).orElseThrow();

        if (!product.getUser().getNickname().equals(nickname)) {
            throw new AccessDeniedException(ExceptionMessage.USER_NOT_AUTHORIZED_PRODUCT);
        }

        productRepository.delete(product);
    }
}
