package org.adriantd.shoppinglist.auth.service;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.dao.UserRepository;
import org.adriantd.shoppinglist.entity.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class SecUserDetailService implements UserDetailsService {

    private final UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User userEntity = (User) userRepository.findByEmail(username).orElse(null);
        if (userEntity == null) {
            throw new UsernameNotFoundException("User not found");
        }

        return userEntity;
    }
}
