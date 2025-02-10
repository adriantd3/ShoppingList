package org.dutylist.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.ColumnDefault;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.dutylist.model.Product;
import org.dutylist.utils.DTO;

import java.io.Serializable;
import java.time.Instant;


@Getter
@Setter
@Entity
@Table(name = "product", indexes = {
        @Index(name = "user_product_idx", columnList = "user_id"),
        @Index(name = "product_category_idx", columnList = "category")
})
public class ProductEntity implements Serializable, DTO<Product> {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Integer id;

    @NotNull
    @ManyToOne(optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "user_id", nullable = false)
    private UserEntity user;

    @Size(max = 255)
    @NotNull
    @Column(name = "name", nullable = false)
    private String name;

    @NotNull
    @ManyToOne(optional = false)
    @JoinColumn(name = "category", nullable = false)
    private CategoryEntity category;

    @Lob
    @Column(name = "image")
    private String image;

    @ColumnDefault("CURRENT_TIMESTAMP")
    @Column(name = "timestamp")
    private Instant timestamp;

    @Lob
    @Column(name = "description")
    private String description;

    @NotNull
    @ColumnDefault("b'1'")
    @Column(name = "user_generated", nullable = false)
    private Boolean userGenerated = false;

    @Override
    public Product toDTO() {
        Product product = new Product();

        product.setId(this.id);
        product.setOwner(this.user.toDTO());
        product.setName(this.name);
        product.setCategory(this.category.getCategory());
        product.setImage(this.image);
        product.setDescription(this.description);
        product.setTimestamp(this.timestamp);
        product.setUserGenerated(this.userGenerated);

        return product;
    }
}