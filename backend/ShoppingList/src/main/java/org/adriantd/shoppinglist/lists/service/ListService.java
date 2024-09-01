package org.adriantd.shoppinglist.lists.service;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.dao.UserRepository;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.lists.dao.ShopListRepository;
import org.adriantd.shoppinglist.lists.dto.lists.ListInfoResponse;
import org.adriantd.shoppinglist.lists.dto.lists.ListRequest;
import org.adriantd.shoppinglist.lists.entity.lists.Shoplist;
import org.adriantd.shoppinglist.utils.DTOService;
import org.adriantd.shoppinglist.utils.ExceptionMessage;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ListService extends DTOService {

    private final ShopListRepository shopListRepository;
    private final UserRepository userRepository;

    public List<ListInfoResponse> getListsFromUser(Integer id){
        User user = userRepository.findById(id).orElseThrow();
        List<Shoplist> lists = shopListRepository.findAllByUser(user);

        return entidadesADTO(lists);
    }

    public List<ListInfoResponse> getListsByIds(List<Integer> ids){
        List<Shoplist> lists = shopListRepository.findAllById(ids);

        return entidadesADTO(lists);
    }

    public ListInfoResponse registerShoplist(ListRequest request, Integer userId){
        User owner = userRepository.findById(userId).orElseThrow();

        Shoplist shoplist = new Shoplist();
        shoplist.setUserOwner(owner);
        shoplist.setName(request.getName());
        shoplist.setType(request.getType());
        shoplist.setNItems(0);
        shoplist.setTimestamp(Instant.now());

        shopListRepository.save(shoplist);

        return shoplist.toDTO();
    }

    public void deleteShoplist(Integer id, Integer userId){
        Shoplist shoplist = shopListRepository.findById(id).orElseThrow();
        User user = userRepository.findById(userId).orElseThrow();

        validateUserAuthorization(shoplist, user);

        shopListRepository.delete(shoplist);
    }

    public void updateShoplist(Integer id, String name, Integer userId){
        Shoplist shoplist = shopListRepository.findById(id).orElseThrow();
        User user = userRepository.findById(userId).orElseThrow();

        validateUserAuthorization(shoplist, user);

        shoplist.setName(name);

        shopListRepository.save(shoplist);
    }

    private boolean isUserOwner(Shoplist shoplist, User user){
        return shoplist.getUserOwner().getId().equals(user.getId());
    }

    private boolean isUserMember(Shoplist shoplist, User user){
        return shoplist.getUsers().contains(user);
    }

    private void validateUserAuthorization(Shoplist shoplist, User user) {
        if (!isUserOwner(shoplist, user) && !isUserMember(shoplist, user)) {
            throw new AccessDeniedException(ExceptionMessage.USER_NOT_AUTHORIZED_LIST);
        }
    }
}
