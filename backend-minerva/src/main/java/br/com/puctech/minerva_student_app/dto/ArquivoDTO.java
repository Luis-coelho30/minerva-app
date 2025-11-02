package br.com.puctech.minerva_student_app.dto;

import br.com.puctech.minerva_student_app.model.Arquivo;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class ArquivoDTO {

    private Long id;
    private Long disciplinaId;
    private String nomeOriginal;
    private String url;
    private String tipo;


    public ArquivoDTO(Arquivo arquivo) {
        this.id = arquivo.getId();
        if(arquivo.getDisciplina() != null) {
            this.disciplinaId = arquivo.getDisciplina().getId();
        }
        this.nomeOriginal = arquivo.getNomeOriginal();
        this.url = arquivo.getUrl();
        this.tipo = arquivo.getTipo();
    }
}
