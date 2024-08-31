package org.adriantd.shoppinglist.lists.dto.items;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ItemRequest {
    @NotNull
    Integer shoplistId;
    @NotNull
    @NotEmpty
    Integer[] productIds;
}
