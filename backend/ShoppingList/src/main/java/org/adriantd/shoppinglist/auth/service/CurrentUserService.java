package org.adriantd.shoppinglist.auth.service;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.dao.UserRepository;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import java.nio.file.AccessDeniedException;

@Service
@RequiredArgsConstructor
public class CurrentUserService {

    private final UserRepository userRepository;

    public UserDetails getCurrentUser() throws AccessDeniedException {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if(authentication == null) {
            throw new AccessDeniedException("LOG: No user authenticated");
        }
        return (UserDetails) authentication.getPrincipal();
    }

    public Integer getCurrentUserId() throws Exception {
        return userRepository.findByNickname(getCurrentUser().getUsername()).orElseThrow().getId();
    }

    public String getCurrentUserNickname() throws AccessDeniedException {
        return getCurrentUser().getUsername();
    }
}
