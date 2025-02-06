package org.openapitools.api;

import lombok.RequiredArgsConstructor;
import org.openapitools.entity.CategoryEntity;
import org.openapitools.entity.ProductEntity;
import org.openapitools.entity.UserEntity;
import org.openapitools.model.NewProduct;
import org.openapitools.model.Product;
import org.openapitools.repository.CategoryRepository;
import org.openapitools.repository.ProductRepository;
import org.openapitools.repository.UserRepository;
import org.openapitools.utils.DTOService;
import org.openapitools.utils.exceptions.ForbiddenException;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@Service
@RequiredArgsConstructor
public class ProductsService extends DTOService {

    private final ProductRepository productRepository;
    private final CategoryRepository categoryRepository;
    private final UserRepository userRepository;

    public Product getProduct(Integer id, Integer userId) {
        ProductEntity product = productRepository.findById(id).orElseThrow();
        if(Objects.equals(product.getUser().getId(), userId)){
            return product.toDTO();
        } else {
            throw new ForbiddenException("User not allowed to access this product");
        }
    }

    public List<Product> searchProduct(Integer userId, String name) {
        String query = name == null || name.isBlank() ? "" : name;
        List<ProductEntity> products = productRepository.searchUserProducts(userId, query).orElse(new ArrayList<>());
        return entidadesADTO(products);
    }

    public Product postProduct(Integer userId, NewProduct newProduct) {
        ProductEntity product = new ProductEntity();
        UserEntity user = userRepository.findById(userId).orElseThrow();
        CategoryEntity category = categoryRepository.findByCodename(newProduct.getCategory()).orElseThrow();

        product.setName(newProduct.getName());
        product.setUser(user);
        product.setCategory(category);
        product.setImage(newProduct.getImage());
        product.setDescription(newProduct.getDescription());
        product.setTimestamp(Instant.now());
        product.setUserGenerated(true);

        productRepository.save(product);

        return product.toDTO();
    }

    public Product updateProduct(Integer id, Integer userId, NewProduct newProduct) {
        ProductEntity product = productRepository.findById(id).orElseThrow();
        if(Objects.equals(product.getUser().getId(), userId)){
            CategoryEntity category = categoryRepository.findByCodename(newProduct.getCategory()).orElseThrow();
            product.setName(newProduct.getName());
            product.setCategory(category);
            product.setImage(newProduct.getImage());
            product.setDescription(newProduct.getDescription());
            productRepository.save(product);
            return product.toDTO();
        } else {
            throw new ForbiddenException("User not allowed to update this product");
        }
    }

    public void deleteProduct(Integer id, Integer userId) {
        ProductEntity product = productRepository.findById(id).orElseThrow();
        if(Objects.equals(product.getUser().getId(), userId)){
            productRepository.delete(product);
        } else {
            throw new ForbiddenException("User not allowed to delete this product");
        }
    }

    public boolean checkProduct(Integer id) {
        ProductEntity product = productRepository.findById(id).orElse(null);
        return product != null;
    }


}
