package org.adriantd.shoppinglist.dao;

import org.adriantd.shoppinglist.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;
import java.util.Optional;

public interface ProductRepository extends JpaRepository<Product, Integer> {
    @Query("select m from Product m where m.user.id = :id")
    Optional<List<Product>> findAllByUserId(Integer id);
}
