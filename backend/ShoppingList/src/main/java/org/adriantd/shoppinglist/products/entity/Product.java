package org.adriantd.shoppinglist.products.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.products.dto.ProductResponse;
import org.adriantd.shoppinglist.utils.DTO;
import org.hibernate.annotations.ColumnDefault;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import java.io.Serializable;
import java.time.Instant;

@Getter
@Setter
@Entity
@Table(name = "product")
public class Product implements Serializable, DTO<ProductResponse> {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Integer id;

    @NotNull
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Size(max = 255)
    @NotNull
    @Column(name = "name", nullable = false)
    private String name;

    @NotNull
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "category", nullable = false)
    private Category category;

    @ColumnDefault("CURRENT_TIMESTAMP")
    @Column(name = "timestamp")
    private Instant timestamp;

    @NotNull
    @ColumnDefault("true")
    @Column(name="user_generated", nullable = false)
    private Boolean userGenerated;

    @Override
    public ProductResponse toDTO() {
        ProductResponse productResponse = new ProductResponse();

        productResponse.setId(this.id);
        productResponse.setOwner(this.user.getUsername());
        productResponse.setName(this.name);
        productResponse.setCategoryId(this.category.getId());
        productResponse.setTimestamp(this.timestamp.toString());
        productResponse.setUserGenerated(this.userGenerated);

        return productResponse;
    }
}