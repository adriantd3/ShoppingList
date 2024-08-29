package org.adriantd.shoppinglist.lists.dao;

import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.lists.entity.lists.Shoplist;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ShopListRepository extends JpaRepository<Shoplist,Integer> {
    @Query("select d from Shoplist d where (d.userOwner = :user) or (:user member of d.users)")
    List<Shoplist> findAllByUser(@Param("user") User user);

    @Query("select d from Shoplist d where (d.userOwner = :user)")
    List<Shoplist> findAllOwnedByUser(@Param("user") User user);
}
