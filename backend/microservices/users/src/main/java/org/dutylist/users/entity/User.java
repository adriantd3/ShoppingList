package org.dutylist.users.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.ColumnDefault;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.io.Serializable;
import java.util.Collection;
import java.util.List;

@Getter
@Setter
@Entity
@Table(name = "user")
public class User implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Integer id;

    @Size(max = 255)
    @NotNull
    @Column(name = "name", nullable = false)
    private String name;

    @Size(max = 255)
    @Column(name = "lastname", nullable = false)
    private String lastname;

    @Size(max = 255)
    @NotNull
    @Column(name = "email", nullable = false)
    private String email;

    @Size(max = 255)
    @Column(name = "password", nullable = false)
    private String password;

    @ColumnDefault("0")
    @Column(name = "premium")
    private Boolean premium;

    @Size(max = 2083)
    @Column(name = "image", nullable = false)
    private String image;

    @NotNull
    @ColumnDefault("'ROLE_USER'")
    @Lob
    @Column(name = "role", nullable = false)
    @Enumerated(EnumType.STRING)
    private RoleType role;
}