package org.adriantd.shoppinglist.utils;

import lombok.Data;
import lombok.NonNull;

@Data
public class ErrorResponse {
    @NonNull
    private String error;
    @NonNull
    private Integer status;
}
