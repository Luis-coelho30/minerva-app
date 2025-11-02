package br.com.puctech.minerva_student_app.dto;

import br.com.puctech.minerva_student_app.model.Nota;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class NotaDTO {

    private Long id;
    private String descricao;
    private Double valor;
    private Integer peso;
    private Long disciplinaId;

    public NotaDTO(Nota nota) {
        this.id = nota.getId();
        this.descricao = nota.getDescricao();
        this.valor = nota.getValor();
        this.peso = nota.getPeso();
        this.disciplinaId = nota.getDisciplina().getId();
    }
}
