package org.dutylist.users.models.request;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserPasswordRequest {
    @NotNull
    private String username;
    @NotNull
    private String password;
}
