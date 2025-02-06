package org.openapitools.utils.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;


import java.util.NoSuchElementException;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException e) {
        String errorMessage = ExceptionMessage.BAD_REQUEST;
        try{
            errorMessage += e.getFieldError().getField() + " " + e.getFieldError().getDefaultMessage();
        } catch (NullPointerException ex) {
            errorMessage = "Bad Request: " + e.getMessage();
        }
        ErrorResponse errorResponse = new ErrorResponse(errorMessage, 400);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(UserException.class)
    public ResponseEntity<ErrorResponse> handleAccessDeniedException(UserException e) {
        String errorMessage = ExceptionMessage.UNAUTHORIZED;
        ErrorResponse errorResponse = new ErrorResponse(errorMessage, 401);

        return new ResponseEntity<>(errorResponse, HttpStatus.UNAUTHORIZED);
    }

    @ExceptionHandler(ForbiddenException.class)
    public ResponseEntity<ErrorResponse> handleAccessDeniedException(ForbiddenException e) {
        String errorMessage = ExceptionMessage.FORBIDDEN;
        ErrorResponse errorResponse = new ErrorResponse(errorMessage, 403);

        return new ResponseEntity<>(errorResponse, HttpStatus.FORBIDDEN);
    }

    @ExceptionHandler(NoSuchElementException.class)
    public ResponseEntity<ErrorResponse> handleNoSuchElementException(NoSuchElementException e) {
        String errorMessage = ExceptionMessage.NOT_FOUND;
        ErrorResponse errorResponse = new ErrorResponse(errorMessage, 404);

        return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
    }


}
