package org.dutylist.users.api.pub;

import org.dutylist.users.models.response.UserPublicInfo;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@Validated
@RequestMapping("/")
public class PublicController implements PublicApi{

    @Override
    public ResponseEntity<List<UserPublicInfo>> getUsersInfo(List<Integer> id) {
        return null;
    }

    @Override
    public ResponseEntity<Void> checkUsersExists(List<Integer> id) {
        return null;
    }
}
