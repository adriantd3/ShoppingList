package org.adriantd.shoppinglist.lists.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.adriantd.shoppinglist.lists.entity.ListType;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ListRequest {
    String name;
    ListType type;
}
