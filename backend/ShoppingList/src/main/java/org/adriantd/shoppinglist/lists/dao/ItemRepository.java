package org.adriantd.shoppinglist.lists.dao;

import org.adriantd.shoppinglist.lists.entity.items.Item;
import org.adriantd.shoppinglist.lists.entity.items.ItemId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.repository.query.Param;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

public interface ItemRepository extends JpaRepository<Item, ItemId> {

    @Query("select i from Item i where i.id.shoplistId = :id")
    List<Item> findAllByShoppingListId(@Param("id")Integer id);

    @Modifying(clearAutomatically = true)
    @Transactional
    @Query("update Item i set i.purchased = :state where i.id.shoplistId = :listId and i.id.productId in :productIds")
    int updateItemStateByListAndProductIds(@Param("listId") Integer listId,
                                            @Param("productIds") List<Integer> productIds,
                                            @Param("state") Boolean state);
}
