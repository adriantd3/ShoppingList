package org.adriantd.shoppinglist.lists.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.adriantd.shoppinglist.lists.entity.ListType;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ListInfoResponse {
    Integer id;
    String owner;
    String name;
    ListType type;
    Integer n_items;
    List<String> members;
    String timestamp;
}
