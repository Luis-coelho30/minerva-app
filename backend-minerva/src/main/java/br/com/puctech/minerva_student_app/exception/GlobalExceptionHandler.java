package br.com.puctech.minerva_student_app.exception;

import br.com.puctech.minerva_student_app.exception.disciplina.DisciplinaNaoEncontradaException;
import br.com.puctech.minerva_student_app.exception.nota.NotaNaoEncontradaException;
import br.com.puctech.minerva_student_app.exception.user.AuthenticationFailedException;
import br.com.puctech.minerva_student_app.exception.user.CredenciaisIncorretasException;
import br.com.puctech.minerva_student_app.exception.user.EmailJaCadastradoException;
import br.com.puctech.minerva_student_app.exception.user.UsuarioNaoEncontradoException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UsernameNotFoundException.class)
    public ResponseEntity<String> handleUsernameNotFoundException(UsernameNotFoundException ex) {
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND) //404
                .body(ex.getMessage());
    }

    @ExceptionHandler(DisciplinaNaoEncontradaException.class)
    public ResponseEntity<String> handleDisciplinaNaoEncontradaException(DisciplinaNaoEncontradaException ex) {
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND) //404
                .body(ex.getMessage());
    }

    @ExceptionHandler(NotaNaoEncontradaException.class)
    public ResponseEntity<String> handleNotaNaoEncontradaException(NotaNaoEncontradaException ex) {
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND) //404
                .body(ex.getMessage());
    }

    @ExceptionHandler(UsuarioNaoEncontradoException.class)
    public ResponseEntity<String> handleUsuarioNaoEncontradoException(UsuarioNaoEncontradoException ex) {
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND) //404
                .body(ex.getMessage());
    }

    @ExceptionHandler(CredenciaisIncorretasException.class)
    public ResponseEntity<String> handleCredenciaisIncorretasException(CredenciaisIncorretasException ex) {
        return ResponseEntity
                .status(HttpStatus.UNAUTHORIZED) //401
                .body(ex.getMessage());
    }

    @ExceptionHandler(AuthenticationFailedException.class)
    public ResponseEntity<String> handleAuthenticationFailedException(AuthenticationFailedException ex) {
        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR) //500
                .body(ex.getMessage());
    }

    @ExceptionHandler(EmailJaCadastradoException.class)
    public ResponseEntity<String> handleEmailJaCadastradoException(EmailJaCadastradoException ex) {
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST) //400
                .body(ex.getMessage());
    }
}
