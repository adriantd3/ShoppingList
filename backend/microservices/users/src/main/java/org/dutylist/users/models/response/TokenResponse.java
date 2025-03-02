package org.dutylist.users.models.response;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class TokenResponse {
    @NotNull
    private String token;

    @NotNull
    @JsonFormat(shape = JsonFormat.Shape.STRING)
    private Instant iat;

    @NotNull
    @JsonFormat(shape = JsonFormat.Shape.STRING)
    private Instant exp;

    @NotNull
    private UserPublicInfo user_info;
}
