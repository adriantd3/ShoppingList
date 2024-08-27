package org.adriantd.shoppinglist.auth.dao;

import org.adriantd.shoppinglist.auth.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Integer> {
    Optional<User> findByNickname(String nickname);
}
