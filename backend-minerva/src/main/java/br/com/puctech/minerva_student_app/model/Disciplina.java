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
public class Disciplina {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "USUARIO_ID", nullable = false)
    private Usuario usuario;
    private String nome;
    private String descricao;
    private Boolean arquivada = false;
    private Double mediaNecessaria;
    private Double mediaAtual;
    private Integer creditos;
    private Integer cargaHorariaTotal = 0;
    private Integer cargaHorariaAula = 0;
    private Integer faltasRegistradas;

    public Disciplina(Usuario usuario, String nome, String descricao, Boolean arquivada, Double mediaNecessaria, Double mediaAtual,
                      Integer creditos, Integer cargaHorariaTotal, Integer cargaHorariaAula, Integer faltasRegistradas) {
        this.usuario = usuario;
        this.nome = nome;
        this.descricao = descricao;
        this.arquivada = arquivada;
        this.mediaNecessaria = mediaNecessaria;
        this.mediaAtual = mediaAtual;
        this.creditos = creditos;
        this.cargaHorariaTotal = cargaHorariaTotal;
        this.cargaHorariaAula = cargaHorariaAula;
        this.faltasRegistradas = faltasRegistradas;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;

        Disciplina that = (Disciplina) o;
        return Objects.equals(getId(), that.getId());
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(getId());
    }
}