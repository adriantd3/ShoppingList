package org.adriantd.shoppinglist.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.Hibernate;

import java.util.Objects;

@Getter
@Setter
@Embeddable
public class ItemId implements java.io.Serializable {
    private static final long serialVersionUID = 8936172174901904352L;
    @NotNull
    @Column(name = "shoplist_id", nullable = false)
    private Integer shoplistId;

    @NotNull
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