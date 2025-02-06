package org.openapitools.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.ColumnDefault;
import org.openapitools.model.UserInfo;
import org.openapitools.utils.DTO;

import java.io.Serializable;
import java.util.LinkedHashSet;
import java.util.Set;

@Getter
@Setter
@Entity
@Table(name = "user", indexes = {
        @Index(name = "user_role_idx", columnList = "role")
}, uniqueConstraints = {
        @UniqueConstraint(name = "username_UNIQUE", columnNames = {"nickname"}),
        @UniqueConstraint(name = "email_UNIQUE", columnNames = {"email"})
})
public class UserEntity implements Serializable, DTO<UserInfo> {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Integer id;

    @Size(max = 255)
    @NotNull
    @Column(name = "nickname", nullable = false)
    private String nickname;

    @Size(max = 255)
    @NotNull
    @Column(name = "name", nullable = false)
    private String name;

    @Size(max = 255)
    @NotNull
    @Column(name = "lastname", nullable = false)
    private String lastname;

    @Size(max = 255)
    @NotNull
    @Column(name = "email", nullable = false)
    private String email;

    @Size(max = 255)
    @NotNull
    @Column(name = "password", nullable = false)
    private String password;

    @ColumnDefault("0")
    @Column(name = "premium")
    private Boolean premium;

    @NotNull
    @ColumnDefault("'ROLE_USER'")
    @Lob
    @Column(name = "role", nullable = false)
    private String role;

    @OneToMany(mappedBy = "user")
    private Set<ProductEntity> products = new LinkedHashSet<>();

    @Override
    public UserInfo toDTO() {
        UserInfo userInfo = new UserInfo();

        userInfo.setId(this.id);
        userInfo.setUsername(this.nickname);
        userInfo.setImage(this.email);

        return userInfo;
    }
}