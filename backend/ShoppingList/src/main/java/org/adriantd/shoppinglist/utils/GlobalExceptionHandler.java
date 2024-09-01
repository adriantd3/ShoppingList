package org.adriantd.shoppinglist.utils;

import com.fasterxml.jackson.core.JsonParseException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.security.InvalidParameterException;
import java.util.NoSuchElementException;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException e) {
        String errorMessage = "Validation error: ";
        errorMessage += e.getFieldError().getField() + " " + e.getFieldError().getDefaultMessage();

        ErrorResponse errorResponse = new ErrorResponse(errorMessage, 400);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(InvalidParameterException.class)
    public ResponseEntity<ErrorResponse> handleInvalidParameterException(InvalidParameterException e) {
        String errorMessage = "Invalid parameter: " + e.getMessage();
        ErrorResponse errorResponse = new ErrorResponse(errorMessage, 400);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(NoSuchElementException.class)
    public ResponseEntity<ErrorResponse> handleNoSuchElementException(NoSuchElementException e) {
        String errorMessage = "Entity not found: " + e.getMessage();
        ErrorResponse errorResponse = new ErrorResponse(errorMessage, 404);

        return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> handleAccessDeniedException(AccessDeniedException e) {
        String errorMessage = "Access denied: " + e.getMessage();
        ErrorResponse errorResponse = new ErrorResponse(errorMessage, 403);

        return new ResponseEntity<>(errorResponse, HttpStatus.FORBIDDEN);
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleHttpMessageNotReadableException(HttpMessageNotReadableException e) {
        String jsonMessage = e.getMessage().startsWith("JSON parse error") ? "JSON parse error on 1 or more attributes" : "";

        if(jsonMessage.isEmpty()) {
            jsonMessage = e.getMessage();
        }

        String errorMessage = "Invalid request body: " + jsonMessage;
        ErrorResponse errorResponse = new ErrorResponse(errorMessage, 400);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

}
