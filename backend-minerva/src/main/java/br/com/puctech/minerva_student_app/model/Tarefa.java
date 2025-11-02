package br.com.puctech.minerva_student_app.model;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;
import java.util.Objects;

@Getter
@Setter
@NoArgsConstructor
@Entity
public class Tarefa {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "USUARIO_ID", nullable = false)
    private Usuario usuario;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "DISCIPLINA_ID")
    private Disciplina disciplina;
    private String titulo;
    private String descricao;
    private String status;
    private LocalDate dataInicio;
    private LocalDate dataFinal;
    private LocalDate concluido_em;
    private String prioridade;
    private Boolean arquivada = false;

    public Tarefa(Usuario usuario, String titulo, String descricao, String status, LocalDate dataInicio, LocalDate dataFinal,
                  LocalDate concluido_em, String prioridade, Boolean arquivada) {
        this.usuario = usuario;
        this.titulo = titulo;
        this.descricao = descricao;
        this.status = status;
        this.dataInicio = dataInicio;
        this.dataFinal = dataFinal;
        this.concluido_em = concluido_em;
        this.prioridade = prioridade;
        this.arquivada = arquivada;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;

        Tarefa tarefa = (Tarefa) o;
        return Objects.equals(getId(), tarefa.getId());
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(getId());
    }
}