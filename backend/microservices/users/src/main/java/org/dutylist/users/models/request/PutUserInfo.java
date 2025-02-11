package org.dutylist.users.models.request;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PutUserInfo {
    @NotNull
    private String name;
    @NotNull
    private String lastname;
    @NotNull
    private String image;
}
