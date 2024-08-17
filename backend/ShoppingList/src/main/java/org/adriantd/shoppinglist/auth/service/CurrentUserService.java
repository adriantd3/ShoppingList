package org.adriantd.shoppinglist.auth.service;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.dao.UserRepository;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CurrentUserService {

    private final UserRepository userRepository;

    public UserDetails getCurrentUser() throws Exception {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if(authentication == null) {
            throw new Exception("LOG: No user authenticated");
        }
        return (UserDetails) authentication.getPrincipal();
    }

    public Integer getCurrentUserId() throws Exception {
        return userRepository.findByNickname(getCurrentUser().getUsername()).orElseThrow().getId();
    }
}
