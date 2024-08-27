package org.adriantd.shoppinglist.lists.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.adriantd.shoppinglist.auth.entity.User;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import java.io.Serializable;

@Getter
@Setter
@Entity
@Table(name = "shoplist_members")
public class ShoplistMember implements Serializable {
    @EmbeddedId
    private ShoplistMemberId id;

    @MapsId("shoplistId")
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "shoplist_id", nullable = false)
    private Shoplist shoplist;

    @MapsId("memberId")
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "member_id", nullable = false)
    private User member;

}