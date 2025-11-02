package br.com.puctech.minerva_student_app.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.Objects;

@Getter
@Setter
@NoArgsConstructor
@Entity
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "DISCIPLINA_ID", nullable = false)
    private Disciplina disciplina;
    private String descricao;
    private Double valor;
    private Integer peso;

    public Nota(String descricao, Double valor, Integer peso) {
        this.descricao = descricao;
        this.valor = valor;
        this.peso = peso;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;

        Nota nota = (Nota) o;
        return Objects.equals(getId(), nota.getId());
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(getId());
    }
}