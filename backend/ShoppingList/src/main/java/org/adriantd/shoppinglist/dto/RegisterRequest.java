package org.adriantd.shoppinglist.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class RegisterRequest {
    String name;
    String lastname;
    String email;
    String password;
}
