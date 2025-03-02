package org.dutylist.users.api.priv;

import org.dutylist.users.models.request.NewUserInfo;
import org.dutylist.users.models.request.PutUserInfo;
import org.dutylist.users.models.response.UserPrivateInfo;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@Validated
@RequestMapping("/private")
public interface PrivateAPI {

    @GetMapping("/{id}")
    public ResponseEntity<UserPrivateInfo> getPrivateUserInfo(@PathVariable Integer id,
                                                              @RequestHeader("user_id") Integer userId);

    @PutMapping("/{id}")
    public ResponseEntity<UserPrivateInfo> updatePrivateUserInfo(@PathVariable Integer id,
                                                                 @RequestHeader("user_id") Integer userId,
                                                                 @RequestBody PutUserInfo putUserInfo);

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Integer id,
                                           @RequestHeader("user_id") Integer userId);

    @PostMapping()
    public ResponseEntity<UserPrivateInfo> createNewUser(@RequestHeader("user_id") Integer userId,
                                                         @RequestBody NewUserInfo newUserInfo);
}
