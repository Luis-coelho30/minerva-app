package br.com.puctech.minerva_student_app.controller;

import br.com.puctech.minerva_student_app.dto.ArquivoDTO;
import br.com.puctech.minerva_student_app.model.Arquivo;
import br.com.puctech.minerva_student_app.model.Usuario;
import br.com.puctech.minerva_student_app.service.ArquivoService;
import br.com.puctech.minerva_student_app.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/arquivos/me")
public class ArquivoController {

    @Autowired
    private ArquivoService arquivoService;

    @Autowired
    private UserService userService;

    @GetMapping
    public List<ArquivoDTO> listarArquivos(Authentication authentication,
                                           @RequestParam(name = "disciplinaId", required = false) Long disciplinaId) {

        List<Arquivo> arquivoList;

        if(disciplinaId == null) {
            arquivoList = arquivoService.listarArquivos(authentication.getName());
        } else {
            arquivoList = arquivoService.listarArquivosPorDisciplina(disciplinaId);
        }

        return arquivoList.stream()
                .map(ArquivoDTO::new)
                .toList();
    }

    @PostMapping
    public ArquivoDTO criarArquivo(@RequestBody ArquivoDTO arquivoDTO, Authentication authentication) {
        Usuario usuario = userService.getUsuario(authentication.getName());

        Arquivo arquivo = new Arquivo(usuario, arquivoDTO.getNomeOriginal(), arquivoDTO.getUrl(), arquivoDTO.getTipo());

        Arquivo arquivoSalvo;

        if(arquivoDTO.getDisciplinaId() == null) {
            arquivoSalvo = arquivoService.salvarArquivo(arquivo);
        } else {
            arquivoSalvo = arquivoService.salvarArquivo(arquivo, arquivoDTO.getDisciplinaId());
        }

        return new ArquivoDTO(arquivoSalvo);
    }

    @PutMapping("/{id}")
    public ArquivoDTO atualizarArquivo(@PathVariable Long id, @RequestBody ArquivoDTO arquivoDTO, Authentication authentication) {
        Usuario usuario = userService.getUsuario(authentication.getName());

        Arquivo arquivo = new Arquivo(usuario, arquivoDTO.getNomeOriginal(), arquivoDTO.getUrl(), arquivoDTO.getTipo());

        Arquivo arquivoSalvo;
        if(arquivoDTO.getDisciplinaId() == null) {
            arquivoSalvo = arquivoService.atualizarArquivo(id, arquivo);
        } else {
            arquivoSalvo = arquivoService.atualizarArquivo(id, arquivo, arquivoDTO.getDisciplinaId());
        }

        return new ArquivoDTO(arquivoSalvo);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletarArquivo(@PathVariable Long id) {
        arquivoService.deletarArquivo(id);
        return ResponseEntity.noContent().build();
    }
}
