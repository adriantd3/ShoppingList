package org.adriantd.shoppinglist.utils;

public class ExceptionMessage {
    public static final String USER_NOT_AUTHORIZED_LIST = "User not member or owner of the list";
    public static final String USER_NOT_AUTHORIZED_PRODUCT = "User not authorized to access product";
    public static final String ITEM_ALREADY_IN_LIST = "Item is already in list";
    public static final String ITEM_NOT_FOUND = "Item not found";
    public static final String USER_NOT_FOUND = "User not found";
    public static final String PRODUCT_NOT_FOUND = "Product not found";
    public static final String SHOP_LIST_NOT_FOUND = "Shop list not found";
    public static final String JWT_TOKEN_REQUIRED = "Authentication token is required for this request";
    public static final String INVALID_JWT_TOKEN = "Invalid authentication token";
    public static final String JWT_TOKEN_EXPIRED = "Authentication token is expired, please login to get a new token";
    public static final String WS_DESTINATION_NOT_FOUND = "WebSocket destination not found or invalid";
}
