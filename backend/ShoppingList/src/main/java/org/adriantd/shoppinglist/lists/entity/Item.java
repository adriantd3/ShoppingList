package org.adriantd.shoppinglist.lists.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.lists.dto.ItemResponse;
import org.adriantd.shoppinglist.products.entity.Product;
import org.adriantd.shoppinglist.utils.DTO;
import org.hibernate.annotations.ColumnDefault;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import java.io.Serializable;

@Getter
@Setter
@Entity
@Table(name = "item")
public class Item implements Serializable, DTO<ItemResponse> {

    @EmbeddedId
    private ItemId id;

    @MapsId("shoplistId")
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "shoplist_id", nullable = false)
    private Shoplist shoplist;

    @MapsId("productId")
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "user", nullable = false)
    private User user;

    @ColumnDefault("1")
    @Column(name = "units", nullable = false)
    private Integer units;

    @Column(name = "type", nullable = false)
    @Enumerated(EnumType.STRING)
    private UnitType type;

    @Override
    public ItemResponse toDTO() {
        return ItemResponse.builder()
                .shoplistId(shoplist.getId())
                .user(user.getNickname())
                .units(units)
                .type(type)
                .product(product.toDTO())
                .build();
    }
}
