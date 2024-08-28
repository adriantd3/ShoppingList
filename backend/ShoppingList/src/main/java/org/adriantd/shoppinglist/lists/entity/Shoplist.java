package org.adriantd.shoppinglist.lists.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.entity.Event;
import org.adriantd.shoppinglist.lists.dto.ListInfoResponse;
import org.adriantd.shoppinglist.utils.DTO;
import org.hibernate.annotations.ColumnDefault;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import java.io.Serializable;
import java.time.Instant;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Getter
@Setter
@Entity
@Table(name = "shoplist")
public class Shoplist implements Serializable, DTO<ListInfoResponse> {
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
    @Column(name = "type", nullable = false)
    @Enumerated(EnumType.STRING)
    private ListType type;

    @ColumnDefault("CURRENT_TIMESTAMP")
    @Column(name = "timestamp")
    private Instant timestamp;

    @ColumnDefault("0")
    @Column(name = "n_items")
    private Integer nItems;

    @ManyToMany
    @JoinTable(name = "shoplist_members",
            joinColumns = @JoinColumn(name = "shoplist_id"),
            inverseJoinColumns = @JoinColumn(name = "member_id"))
    private List<User> users = new ArrayList<>();

    @Override
    public ListInfoResponse toDTO() {
        List<String> members = new ArrayList<>();
        for(User member : users){
            members.add(member.getNickname());
        }

        return ListInfoResponse.builder()
                .id(id)
                .owner(userOwner.getNickname())
                .name(name)
                .members(members)
                .type(type)
                .n_items(nItems)
                .timestamp(timestamp.toString())
                .build();
    }
}