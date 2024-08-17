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
    Integer userId;
    String name;
    String image;
    String magnitude;
    String timestamp;
}
