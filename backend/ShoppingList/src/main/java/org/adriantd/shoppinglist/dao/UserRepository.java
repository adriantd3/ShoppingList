package org.adriantd.shoppinglist.dao;

import org.adriantd.shoppinglist.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Integer> {
    Optional<User> findByNickname(String nickname);
}
