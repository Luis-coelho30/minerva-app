package br.com.puctech.minerva_student_app.exception.user;

public class UsuarioNaoEncontradoException extends RuntimeException {
    public UsuarioNaoEncontradoException(String email) {
        super("Usuário com email: " + email + " não foi encontrado");
    }
}
