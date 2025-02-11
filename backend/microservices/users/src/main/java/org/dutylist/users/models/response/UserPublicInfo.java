package org.dutylist.users.models.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import jakarta;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserPublicInfo {
    private Integer id;
    private String username;
    private String image;
}
