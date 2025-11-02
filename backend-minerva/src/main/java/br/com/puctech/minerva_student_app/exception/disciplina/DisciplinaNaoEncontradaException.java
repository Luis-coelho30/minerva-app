package br.com.puctech.minerva_student_app.exception.disciplina;

public class DisciplinaNaoEncontradaException extends RuntimeException {
    public DisciplinaNaoEncontradaException(Long id) {
        super("Disciplina " + id + " não foi encontrada.");
    }
}
