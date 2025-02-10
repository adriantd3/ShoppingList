package org.dutylist.repository;

import org.dutylist.entity.CategoryEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.Optional;

public interface CategoryRepository extends JpaRepository<CategoryEntity, Integer> {
    @Query("select c from CategoryEntity c where c.category = :codename")
    Optional<CategoryEntity> findByCodename(String codename);
}
