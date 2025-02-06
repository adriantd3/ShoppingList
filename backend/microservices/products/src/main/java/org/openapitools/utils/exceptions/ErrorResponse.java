package org.openapitools.utils.exceptions;

import lombok.Data;
import lombok.NonNull;

@Data
public class ErrorResponse {
    @NonNull
    private String error;
    @NonNull
    private Integer status;
}
