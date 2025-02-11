package org.dutylist.users.models.response;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserPrivateInfo {
    @NotNull
    private Integer id;
    @NotNull
    private String username;
    @NotNull
    private String name;
    @NotNull
    private String lastname;
    @NotNull
    private String email;
    @NotNull
    private Boolean password;
    @NotNull
    private String image;
}
