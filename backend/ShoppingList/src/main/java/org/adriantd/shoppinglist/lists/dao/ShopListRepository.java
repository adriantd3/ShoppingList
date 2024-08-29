package org.adriantd.shoppinglist.lists.dao;

import org.adriantd.shoppinglist.lists.entity.lists.Shoplist;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ShopListRepository extends JpaRepository<Shoplist,Integer> {
}
