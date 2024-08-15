package org.adriantd.shoppinglist.auth.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class AuthResponse {
    String token;
}
