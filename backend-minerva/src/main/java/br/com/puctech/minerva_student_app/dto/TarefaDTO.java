package br.com.puctech.minerva_student_app.dto;

import br.com.puctech.minerva_student_app.model.Tarefa;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
public class TarefaDTO {

    private Long id;
    private String titulo;
    private String descricao;
    private String status;
    private Long disciplinaId;
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "dd/MM/yyyy")
    private LocalDate dataInicio;
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "dd/MM/yyyy")
    private LocalDate dataFinal;
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "dd/MM/yyyy")
    private LocalDate concluido_em;
    private String prioridade;
    private Boolean arquivada;

    public TarefaDTO(Tarefa tarefa) {
        this.id = tarefa.getId();
        this.titulo = tarefa.getTitulo();
        this.descricao = tarefa.getDescricao();
        this.status = tarefa.getStatus();
        if(tarefa.getDisciplina() != null) {
            this.disciplinaId = tarefa.getDisciplina().getId();
        }
        this.dataInicio = tarefa.getDataInicio();
        this.dataFinal = tarefa.getDataFinal();
        this.concluido_em = tarefa.getConcluido_em();
        this.prioridade = tarefa.getPrioridade();
        this.arquivada = tarefa.getArquivada();
    }
}
