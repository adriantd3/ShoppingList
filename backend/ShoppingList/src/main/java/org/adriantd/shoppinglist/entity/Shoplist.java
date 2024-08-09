package org.adriantd.shoppinglist.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.ColumnDefault;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import java.time.Instant;
import java.util.LinkedHashSet;
import java.util.Set;

@Getter
@Setter
@Entity
@Table(name = "shoplist")
public class Shoplist {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Integer id;

    @NotNull
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "user_owner_id", nullable = false)
    private User userOwner;

    @Size(max = 45)
    @NotNull
    @Column(name = "name", nullable = false, length = 45)
    private String name;

    @NotNull
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "type", nullable = false)
    private ShoplistType type;

    @ColumnDefault("CURRENT_TIMESTAMP")
    @Column(name = "timestamp")
    private Instant timestamp;

    @ColumnDefault("0")
    @Column(name = "n_items")
    private Integer nItems;

    @OneToMany(mappedBy = "shoplist")
    private Set<Event> events = new LinkedHashSet<>();

    @OneToMany(mappedBy = "shoplist")
    private Set<Item> items = new LinkedHashSet<>();

    @ManyToMany
    @JoinTable(name = "shoplist_members",
            joinColumns = @JoinColumn(name = "shoplist_id"),
            inverseJoinColumns = @JoinColumn(name = "member_id"))
    private Set<User> users = new LinkedHashSet<>();

}