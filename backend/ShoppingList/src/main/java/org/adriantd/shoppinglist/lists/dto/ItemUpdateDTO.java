package org.adriantd.shoppinglist.lists.dto;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.adriantd.shoppinglist.lists.entity.items.UnitType;
import org.adriantd.shoppinglist.products.dto.ProductResponse;

@Data
@AllArgsConstructor
public class ItemUpdateDTO {
    @NotNull
    EventType eventType;
    @NotNull
    Integer productId;

    String user;
    Integer units;
    UnitType type;
    Boolean purchased;
    String description;
}