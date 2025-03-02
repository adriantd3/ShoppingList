package org.dutylist.users.api.priv;

import org.dutylist.users.models.request.NewUserInfo;
import org.dutylist.users.models.request.PutUserInfo;
import org.dutylist.users.models.response.UserPrivateInfo;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Validated
@RequestMapping("/private")
public class PrivateController implements PrivateAPI{

    @Override
    public ResponseEntity<UserPrivateInfo> getPrivateUserInfo(Integer id, Integer userId) {
        return null;
    }

    @Override
    public ResponseEntity<UserPrivateInfo> updatePrivateUserInfo(Integer id, Integer userId, PutUserInfo putUserInfo) {
        return null;
    }

    @Override
    public ResponseEntity<Void> deleteUser(Integer id, Integer userId) {
        return null;
    }

    @Override
    public ResponseEntity<UserPrivateInfo> createNewUser(Integer userId, NewUserInfo newUserInfo) {
        return null;
    }
}
