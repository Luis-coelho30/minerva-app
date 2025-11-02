package br.com.puctech.minerva_student_app.controller;

import br.com.puctech.minerva_student_app.dto.TarefaDTO;
import br.com.puctech.minerva_student_app.model.Tarefa;
import br.com.puctech.minerva_student_app.model.Usuario;
import br.com.puctech.minerva_student_app.service.TarefaService;
import br.com.puctech.minerva_student_app.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/tarefas/me")
public class TarefaController {

    @Autowired
    private TarefaService tarefaService;

    @Autowired
    private UserService userService;

    @GetMapping
    public List<TarefaDTO> listarTarefasPorUsuario(Authentication authentication,
                                                   @RequestParam(name = "disciplinaId", required = false) Long disciplinaId) {
        List<Tarefa> tarefaList = tarefaService.listarTarefasPorUsuario(authentication.getName());

        if(disciplinaId == null) {
            tarefaList = tarefaService.listarTarefasPorUsuario(authentication.getName());
        } else {
            tarefaList = tarefaService.buscarPorDisciplina(authentication.getName(), disciplinaId);
        }

        return tarefaList.stream()
                .map(TarefaDTO::new)
                .toList();
    }

    @PostMapping
    public TarefaDTO criarTarefa(@RequestBody TarefaDTO tarefaDTO, Authentication authentication) {
        Usuario usuario = userService.getUsuario(authentication.getName());

        Tarefa tarefa = new Tarefa(usuario, tarefaDTO.getTitulo(), tarefaDTO.getDescricao(),
                tarefaDTO.getStatus(), tarefaDTO.getDataInicio(), tarefaDTO.getDataFinal(), tarefaDTO.getConcluido_em(),
                tarefaDTO.getPrioridade(), tarefaDTO.getArquivada());

        Tarefa tarefaSalva;

        if(tarefaDTO.getDisciplinaId() == null) {
            tarefaSalva = tarefaService.salvarTarefa(tarefa);
        } else {
            tarefaSalva = tarefaService.salvarTarefa(tarefa, tarefaDTO.getDisciplinaId());
        }

        return new TarefaDTO(tarefaSalva);
    }

    @PutMapping("/{id}")
    public TarefaDTO atualizarTarefa(@PathVariable Long id, @RequestBody TarefaDTO tarefaDTO, Authentication authentication) {
        Usuario usuario = userService.getUsuario(authentication.getName());

        Tarefa tarefa = new Tarefa(usuario, tarefaDTO.getTitulo(), tarefaDTO.getDescricao(),
                tarefaDTO.getStatus(), tarefaDTO.getDataInicio(), tarefaDTO.getDataFinal(), tarefaDTO.getConcluido_em(),
                tarefaDTO.getPrioridade(), tarefaDTO.getArquivada());

        Tarefa tarefaSalva;

        if(tarefaDTO.getDisciplinaId() == null) {
            tarefaSalva = tarefaService.atualizarTarefa(id, tarefa);
        } else {
            tarefaSalva = tarefaService.atualizarTarefa(id, tarefa, tarefaDTO.getDisciplinaId());
        }

        return new TarefaDTO(tarefaSalva);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletarTarefa(@PathVariable Long id) {
        tarefaService.deletarTarefa(id);
        return ResponseEntity.noContent().build();
    }
}
