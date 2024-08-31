package org.adriantd.shoppinglist.lists.dto.items;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.adriantd.shoppinglist.lists.entity.items.UnitType;

@Data
@Builder
@AllArgsConstructor
public class RegisterItemRequest {
    @NotNull
    Integer shoplistId;
    @NotNull
    Integer productId;
    @NotNull
    Integer units;
    @NotNull
    UnitType type;
}
