package org.adriantd.shoppinglist.products.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ProductResponse {
    Integer id;
    String owner;
    String name;
    Integer categoryId;
    String timestamp;
    Boolean userGenerated;
}
