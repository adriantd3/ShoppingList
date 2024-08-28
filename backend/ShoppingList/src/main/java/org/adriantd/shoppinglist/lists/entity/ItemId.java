package org.adriantd.shoppinglist.lists.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.Hibernate;

import java.io.Serializable;
import java.util.Objects;

@Getter
@Setter
@Embeddable
@NoArgsConstructor
@AllArgsConstructor
public class ItemId implements Serializable {
    private static final long serialVersionUID = 821659352773943243L;
    @Column(name = "shoplist_id", nullable = false)
    private Integer shoplistId;

    @Column(name = "product_id", nullable = false)
    private Integer productId;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) return false;
        ItemId entity = (ItemId) o;
        return Objects.equals(this.productId, entity.productId) &&
                Objects.equals(this.shoplistId, entity.shoplistId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(productId, shoplistId);
    }

}
