package br.com.puctech.minerva_student_app.exception.user;

public class CredenciaisIncorretasException extends RuntimeException {
    public CredenciaisIncorretasException(String message) {
        super(message);
    }
}
