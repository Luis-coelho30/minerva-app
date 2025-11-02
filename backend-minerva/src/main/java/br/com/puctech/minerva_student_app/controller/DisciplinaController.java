package br.com.puctech.minerva_student_app.controller;

import br.com.puctech.minerva_student_app.dto.DisciplinaDTO;
import br.com.puctech.minerva_student_app.model.Disciplina;
import br.com.puctech.minerva_student_app.model.Usuario;
import br.com.puctech.minerva_student_app.service.DisciplinaService;
import br.com.puctech.minerva_student_app.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/disciplinas/me")
public class DisciplinaController {

    @Autowired
    private DisciplinaService disciplinaService;

    @Autowired
    private UserService userService;

    @GetMapping
    public List<DisciplinaDTO> listarDisciplinas(Authentication authentication) {
        List<Disciplina> disciplina = disciplinaService.listarDisciplinas(authentication.getName());

        return disciplina.stream().map(DisciplinaDTO::new).toList();
    }

    @GetMapping("/{id}")
    public ResponseEntity<DisciplinaDTO> buscarPorId(@PathVariable Long id, Authentication authentication) {
        return disciplinaService.buscarPorId(id)
                .map(disciplina -> ResponseEntity.ok(new DisciplinaDTO(disciplina)))
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public DisciplinaDTO criarDisciplina(Authentication authentication, @RequestBody DisciplinaDTO disciplinaDTO) {
        Usuario usuario = userService.getUsuario(authentication.getName());

        Disciplina disciplina = new Disciplina(usuario, disciplinaDTO.getNome(), disciplinaDTO.getDescricao(), disciplinaDTO.getArquivada(),
                disciplinaDTO.getMediaNecessaria(), 0.0, disciplinaDTO.getCreditos(), disciplinaDTO.getCargaHorariaTotal(),
                disciplinaDTO.getCargaHorariaAula(), disciplinaDTO.getFaltasRegistradas());
        Disciplina disciplinaSalva = disciplinaService.salvarDisciplina(disciplina);

        return new DisciplinaDTO(disciplinaSalva);
    }

    @PutMapping("/{id}")
    public DisciplinaDTO atualizarDisciplina(@PathVariable Long id, @RequestBody DisciplinaDTO disciplinaDTO, Authentication authentication) {
        Usuario usuario = userService.getUsuario(authentication.getName());

        Disciplina disciplina = new Disciplina(usuario, disciplinaDTO.getNome(), disciplinaDTO.getDescricao(), disciplinaDTO.getArquivada(),
                disciplinaDTO.getMediaNecessaria(), disciplinaDTO.getMediaAtual(), disciplinaDTO.getCreditos(), disciplinaDTO.getCargaHorariaTotal(),
                disciplinaDTO.getCargaHorariaAula(), disciplinaDTO.getFaltasRegistradas());
        Disciplina disciplinaSalva = disciplinaService.atualizarDisciplina(id, disciplina);

        return new DisciplinaDTO(disciplinaSalva);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletarDisciplina(@PathVariable Long id, Authentication authentication) {
        disciplinaService.deletarDisciplina(id);
        return ResponseEntity.noContent().build();
    }
}
