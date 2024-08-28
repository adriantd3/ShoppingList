package org.adriantd.shoppinglist.lists.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.adriantd.shoppinglist.lists.entity.UnitType;
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
}
