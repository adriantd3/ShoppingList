package org.adriantd.shoppinglist.lists.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.adriantd.shoppinglist.lists.entity.UnitType;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RegisterItemRequest {
    Integer shoplistId;
    Integer productId;
    Integer units;
    UnitType type;
}
