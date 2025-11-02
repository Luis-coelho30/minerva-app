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
public class Arquivo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "USUARIO_ID", nullable = false)
    private Usuario usuario;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "DISCIPLINA_ID", nullable = true)
    private Disciplina disciplina;
    private String nomeOriginal;
    private String url;
    private String tipo;

    public Arquivo(Usuario usuario, String nomeOriginal, String url, String tipo) {
        this.usuario = usuario;
        this.nomeOriginal = nomeOriginal;
        this.url = url;
        this.tipo = tipo;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;

        Arquivo arquivo = (Arquivo) o;
        return Objects.equals(getId(), arquivo.getId());
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(getId());
    }
}