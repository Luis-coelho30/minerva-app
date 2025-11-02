package br.com.puctech.minerva_student_app.dto;

import br.com.puctech.minerva_student_app.model.Disciplina;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.beans.BeanUtils;

@Getter
@Setter
@NoArgsConstructor
public class DisciplinaDTO {

    private Long id;
    private String nome;
    private String descricao;
    private Boolean arquivada;
    private Double mediaNecessaria;
    private Double mediaAtual;
    private Integer creditos;
    private Integer cargaHorariaTotal;
    private Integer cargaHorariaAula;
    private Integer faltasRegistradas;

    public DisciplinaDTO(Disciplina disciplina) {
        BeanUtils.copyProperties(disciplina, this);
    }
}
