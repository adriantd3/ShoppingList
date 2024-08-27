package org.adriantd.shoppinglist.lists.dao;

import org.adriantd.shoppinglist.lists.entity.Shoplist;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ShopListRepository extends JpaRepository<Shoplist,Integer> {
}
