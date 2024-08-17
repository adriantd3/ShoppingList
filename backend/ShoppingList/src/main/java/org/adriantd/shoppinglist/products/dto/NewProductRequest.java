package org.adriantd.shoppinglist.products.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NewProductRequest {
    String name;
    String image;
    String magnitude;
}
