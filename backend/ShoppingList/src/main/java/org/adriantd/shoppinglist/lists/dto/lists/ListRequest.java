package org.adriantd.shoppinglist.lists.dto.lists;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.adriantd.shoppinglist.lists.entity.lists.ListType;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ListRequest {
    @NotNull
    String name;
    @NotNull
    ListType type;
}
