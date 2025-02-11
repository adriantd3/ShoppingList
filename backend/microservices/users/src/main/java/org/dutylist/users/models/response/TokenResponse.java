package org.dutylist.users.models.response;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class TokenResponse {
    @NotNull
    private String token;
    @NotNull
    private String iat;
    @NotNull
    private String exp;
    @NotNull
    private UserPublicInfo user_info;
}
