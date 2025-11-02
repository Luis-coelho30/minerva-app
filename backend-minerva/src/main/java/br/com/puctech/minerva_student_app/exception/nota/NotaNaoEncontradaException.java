package br.com.puctech.minerva_student_app.exception.nota;

public class NotaNaoEncontradaException extends RuntimeException {
    public NotaNaoEncontradaException(Long id) {
        super("Nota com ID: " + id + " não foi encontrada.");
    }
}
