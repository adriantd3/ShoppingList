package org.dutylist.users.api;

import org.dutylist.users.models.response.UserPublicInfo;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@Validated
@RequestMapping("/")
public interface PublicApi {

    @GetMapping()
    public ResponseEntity<List<UserPublicInfo>> getUsersInfo(List<Integer> id);

    @RequestMapping(method = RequestMethod.HEAD)
    public ResponseEntity<Void> checkUsersExists(List<Integer> id);

}
