package org.adriantd.shoppinglist.products.dao;

import org.adriantd.shoppinglist.products.entity.Category;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CategoryRepository extends JpaRepository<Category,Integer> {
}
