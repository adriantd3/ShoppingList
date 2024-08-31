package org.adriantd.shoppinglist.utils;

import lombok.Data;
import lombok.NonNull;

@Data
public class ErrorResponse {
    @NonNull
    private String message;
    @NonNull
    private Integer statusCode;

    @Override
    public String toString() {
        return String.format("ERROR %d: %s", statusCode, message);
    }
}
