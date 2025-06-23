package org.adriantd.shoppinglist.lists.dto.items;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.adriantd.shoppinglist.lists.entity.items.UnitType;
import org.adriantd.shoppinglist.products.dto.ProductResponse;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ItemResponse {
    Integer shoplistId;
    String user;
    Integer units;
    UnitType type;
    ProductResponse product;
    Boolean purchased;
    String description;
}
