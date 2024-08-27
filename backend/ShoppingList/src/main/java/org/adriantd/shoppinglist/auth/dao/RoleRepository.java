package org.adriantd.shoppinglist.auth.dao;

import org.adriantd.shoppinglist.auth.entity.Role;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RoleRepository extends JpaRepository<Role,Integer> {
}
