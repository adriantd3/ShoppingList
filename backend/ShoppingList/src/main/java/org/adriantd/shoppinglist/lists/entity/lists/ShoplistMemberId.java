package org.adriantd.shoppinglist.lists.entity.lists;

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
public class ShoplistMemberId implements java.io.Serializable {
    private static final long serialVersionUID = -2739229283850398895L;
    @NotNull
    @Column(name = "shoplist_id", nullable = false)
    private Integer shoplistId;

    @NotNull
    @Column(name = "member_id", nullable = false)
    private Integer memberId;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) return false;
        ShoplistMemberId entity = (ShoplistMemberId) o;
        return Objects.equals(this.shoplistId, entity.shoplistId) &&
                Objects.equals(this.memberId, entity.memberId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(shoplistId, memberId);
    }

}