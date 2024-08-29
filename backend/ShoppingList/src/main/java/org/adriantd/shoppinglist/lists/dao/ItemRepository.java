package org.adriantd.shoppinglist.lists.dao;

import org.adriantd.shoppinglist.lists.entity.items.Item;
import org.adriantd.shoppinglist.lists.entity.items.ItemId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ItemRepository extends JpaRepository<Item, ItemId> {

    @Query("select i from Item i where i.id.shoplistId = :id")
    List<Item> findAllByShoppingListId(@Param("id")Integer id);
}
