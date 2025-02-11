package org.openapitools.repository;

import org.openapitools.entity.ProductEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;
import java.util.Optional;

public interface ProductRepository extends JpaRepository<ProductEntity, Integer> {
    @Query("select m from ProductEntity m where m.user.id = :id and lower(m.name) like %:name%")
    Optional<List<ProductEntity>> searchUserProducts(Integer id, String name);
}
