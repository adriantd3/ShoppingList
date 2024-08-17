package org.adriantd.shoppinglist.dao;

import org.adriantd.shoppinglist.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepository extends JpaRepository<Product, Integer> {
}
