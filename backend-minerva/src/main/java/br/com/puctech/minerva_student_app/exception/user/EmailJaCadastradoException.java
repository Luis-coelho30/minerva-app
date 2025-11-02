package br.com.puctech.minerva_student_app.exception.user;

public class EmailJaCadastradoException extends RuntimeException {
    public EmailJaCadastradoException(String email) {
        super("O email: " + email + " já foi cadastrado.");
    }
}
