package br.com.puctech.minerva_student_app.controller;

import br.com.puctech.minerva_student_app.dto.NotaDTO;
import br.com.puctech.minerva_student_app.model.Nota;
import br.com.puctech.minerva_student_app.service.NotaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/notas/me")
public class NotaController {

    @Autowired
    private NotaService notaService;

    @GetMapping("/disciplina/{disciplinaId}")
    public List<NotaDTO> listarNotas(@PathVariable Long disciplinaId) {
        List<Nota> nota = notaService.listarNotasPorDisciplina(disciplinaId);

        return nota.stream()
                .map(NotaDTO::new)
                .toList();
    }

    @GetMapping("/agrupadas")
    public Map<Long, List<NotaDTO>> getNotasAgrupadasPorDisc(Authentication authentication) {

        String email = authentication.getName();
        Map<Long, List<Nota>> mapaDeNotas = notaService.listarNotasAgrupadasPorDisciplina(email);

        return mapaDeNotas.entrySet().stream()
                .collect(Collectors.toMap(
                        Map.Entry::getKey,
                        entry -> entry.getValue().stream()
                                .map(NotaDTO::new)
                                .collect(Collectors.toList())
                ));
    }

    @PostMapping
    public NotaDTO criarNota(@RequestBody NotaDTO notaDTO) {
        Nota nota = new Nota(notaDTO.getDescricao(), notaDTO.getValor(), notaDTO.getPeso());
        Nota notaSalva = notaService.salvarNota(nota, notaDTO.getDisciplinaId());

        return new NotaDTO(notaSalva);
    }

    @PutMapping("/{id}")
    public NotaDTO atualizarNota(@PathVariable Long id, @RequestBody NotaDTO notaDTO) {
        Nota nota = new Nota(notaDTO.getDescricao(), notaDTO.getValor(), notaDTO.getPeso());
        Nota notaSalva = notaService.atualizarNota(id, nota, notaDTO.getDisciplinaId());

        return new NotaDTO(notaSalva);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletarNota(@PathVariable Long id) {
        notaService.deletarNota(id);
        return ResponseEntity.noContent().build();
    }
}
