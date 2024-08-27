package org.adriantd.shoppinglist.lists;

import lombok.RequiredArgsConstructor;
import org.adriantd.shoppinglist.auth.dao.UserRepository;
import org.adriantd.shoppinglist.auth.entity.User;
import org.adriantd.shoppinglist.lists.dao.ShopListRepository;
import org.adriantd.shoppinglist.lists.dto.ListInfoResponse;
import org.adriantd.shoppinglist.lists.dto.ListRequest;
import org.adriantd.shoppinglist.lists.entity.Shoplist;
import org.springframework.stereotype.Service;

import java.sql.Timestamp;
import java.time.Instant;
import java.util.ArrayList;

@Service
@RequiredArgsConstructor
public class ListService {

    private final ShopListRepository shopListRepository;
    private final UserRepository userRepository;

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

}
