package org.dutylist.users.models.request;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class NewUserInfo {
    @NotNull
    private String username;
    @NotNull
    private String name;
    @NotNull
    private String lastname;
    @NotNull
    private String email;
    @NotNull
    private String password;
}
