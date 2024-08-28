package org.adriantd.shoppinglist.auth.service;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.dao.UserRepository;
import org.adriantd.shoppinglist.auth.entity.User;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import java.nio.file.AccessDeniedException;
import java.util.List;
import java.util.stream.Collectors;

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

    public Integer getCurrentUserId() throws AccessDeniedException {
        return userRepository.findByNickname(getCurrentUser().getUsername()).orElseThrow().getId();
    }

    public String getCurrentUserNickname() throws AccessDeniedException {
        return getCurrentUser().getUsername();
    }

    public List<String> usersNicknames(List<User> users){
        return users.stream().map(User::getNickname).collect(Collectors.toList());
    }
}
