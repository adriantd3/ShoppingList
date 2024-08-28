package org.adriantd.shoppinglist.lists.dao;

import org.adriantd.shoppinglist.lists.entity.Item;
import org.adriantd.shoppinglist.lists.entity.ItemId;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ItemRepository extends JpaRepository<Item, ItemId> {
}
