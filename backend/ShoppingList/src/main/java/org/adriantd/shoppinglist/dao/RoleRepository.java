package org.adriantd.shoppinglist.dao;

import org.adriantd.shoppinglist.entity.Role;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RoleRepository extends JpaRepository<Role,Integer> {
}
